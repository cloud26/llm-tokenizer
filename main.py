import asyncio
import logging
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="LLM Tokenizer API",
    description="A FastAPI service for tokenizing text using Hugging Face transformers",
    version="1.0.0"
)

# 服务端 tokenizer 缓存
tokenizer_cache: Dict[str, Any] = {}


class TokenizeRequest(BaseModel):
    text: str
    hubPath: str


class TokenizeResponse(BaseModel):
    success: bool
    tokenCount: int
    tokens: List[str]
    tokenIds: List[int]


class ErrorResponse(BaseModel):
    error: str
    details: str = None


async def load_tokenizer(hub_path: str) -> Any:
    """加载 Hugging Face tokenizer"""
    try:
        # 检查缓存
        if hub_path in tokenizer_cache:
            logger.info(f"Using cached tokenizer: {hub_path}")
            return tokenizer_cache[hub_path]

        logger.info(f"Loading tokenizer: {hub_path}")

        # 在线程池中加载 tokenizer 以避免阻塞
        loop = asyncio.get_event_loop()
        tokenizer = await loop.run_in_executor(
            None,
            AutoTokenizer.from_pretrained,
            hub_path
        )

        # 缓存 tokenizer
        tokenizer_cache[hub_path] = tokenizer
        logger.info(f"Successfully loaded and cached tokenizer: {hub_path}")

        return tokenizer

    except Exception as error:
        logger.error(f"Failed to load tokenizer {hub_path}: {str(error)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load {hub_path}: {str(error)}"
        )


@app.post("/tokenize", response_model=TokenizeResponse)
async def tokenize_text(request: TokenizeRequest):
    """对文本进行 tokenization"""
    try:
        if not request.text or not request.hubPath:
            raise HTTPException(
                status_code=400,
                detail="Missing text or hubPath parameter"
            )

        # 加载对应的 tokenizer
        tokenizer = await load_tokenizer(request.hubPath)

        # 在线程池中进行 tokenization 以避免阻塞
        loop = asyncio.get_event_loop()

        # 进行 tokenization
        encoded = await loop.run_in_executor(
            None,
            tokenizer.encode,
            request.text
        )

        tokens = await loop.run_in_executor(
            None,
            tokenizer.tokenize,
            request.text
        )

        return TokenizeResponse(
            success=True,
            tokenCount=len(encoded),
            tokens=tokens,
            tokenIds=encoded
        )

    except HTTPException:
        # 重新抛出 HTTPException
        raise
    except Exception as error:
        logger.error(f"Tokenization error: {str(error)}")
        raise HTTPException(
            status_code=500,
            detail=f"Tokenization failed: {str(error)}"
        )


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "cache_size": len(tokenizer_cache)}


@app.get("/cache")
async def get_cache_info():
    """获取缓存信息"""
    return {
        "cached_models": list(tokenizer_cache.keys()),
        "cache_size": len(tokenizer_cache)
    }


@app.delete("/cache")
async def clear_cache():
    """清除缓存"""
    global tokenizer_cache
    cache_size = len(tokenizer_cache)
    tokenizer_cache.clear()
    logger.info(f"Cleared {cache_size} tokenizers from cache")
    return {"message": f"Cleared {cache_size} tokenizers from cache"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
