# LLM Tokenizer FastAPI Service

这是一个基于 FastAPI 的 Hugging Face Tokenizer 服务，提供了高性能的文本 tokenization 功能，支持缓存和异步处理。

## 功能特性

- 🚀 **高性能异步处理**: 使用 FastAPI 和异步编程，支持高并发请求
- 💾 **智能缓存机制**: 自动缓存已加载的 tokenizer，避免重复加载
- 🔄 **多模型支持**: 支持 Hugging Face Hub 上的所有 tokenizer 模型
- 📊 **详细的响应信息**: 返回 token 数量、tokens 列表和 token IDs
- 🛠️ **完整的错误处理**: 友好的错误信息和状态码
- 📈 **监控端点**: 提供健康检查和缓存状态查询

## 安装依赖

首先确保您已经安装了 Python 3.8+，然后安装依赖：

```bash
pip install -r requirements.txt
```

## 启动服务

### 方法 1: 直接运行

```bash
python main.py
```

### 方法 2: 使用 uvicorn

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

服务将在 `http://localhost:8000` 上启动。

## API 文档

启动服务后，您可以访问以下地址查看自动生成的 API 文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API 端点

### 1. 文本 Tokenization

**POST** `/tokenize`

将文本转换为 tokens。

**请求体:**
```json
{
    "text": "Hello, how are you today?",
    "hubPath": "bert-base-uncased"
}
```

**响应:**
```json
{
    "success": true,
    "tokenCount": 8,
    "tokens": ["hello", ",", "how", "are", "you", "today", "?"],
    "tokenIds": [7592, 1010, 2129, 2024, 2017, 2651, 1029]
}
```

### 2. 健康检查

**GET** `/health`

检查服务状态。

**响应:**
```json
{
    "status": "healthy",
    "cache_size": 3
}
```

### 3. 缓存信息

**GET** `/cache`

查看当前缓存的模型信息。

**响应:**
```json
{
    "cached_models": ["bert-base-uncased", "gpt2", "distilbert-base-uncased"],
    "cache_size": 3
}
```

### 4. 清除缓存

**DELETE** `/cache`

清除所有缓存的 tokenizer。

**响应:**
```json
{
    "message": "Cleared 3 tokenizers from cache"
}
```

## 支持的模型

该服务支持 Hugging Face Hub 上的所有 tokenizer 模型，包括但不限于：

- `bert-base-uncased`
- `bert-large-uncased`
- `gpt2`
- `distilbert-base-uncased`
- `roberta-base`
- `t5-small`
- `microsoft/DialoGPT-medium`
- 等等...

## 使用示例

### Python 客户端示例

```python
import requests

# API 基础 URL
BASE_URL = "http://localhost:8000"

# 发送 tokenization 请求
response = requests.post(
    f"{BASE_URL}/tokenize",
    json={
        "text": "Hello, world!",
        "hubPath": "bert-base-uncased"
    }
)

if response.status_code == 200:
    result = response.json()
    print(f"Token count: {result['tokenCount']}")
    print(f"Tokens: {result['tokens']}")
else:
    print(f"Error: {response.text}")
```

### cURL 示例

```bash
curl -X POST "http://localhost:8000/tokenize" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Hello, world!",
       "hubPath": "bert-base-uncased"
     }'
```

### JavaScript/Fetch 示例

```javascript
const response = await fetch('http://localhost:8000/tokenize', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        text: 'Hello, world!',
        hubPath: 'bert-base-uncased'
    })
});

const result = await response.json();
console.log('Token count:', result.tokenCount);
console.log('Tokens:', result.tokens);
```

## 测试

运行测试脚本来验证服务功能：

```bash
# 确保服务已启动，然后运行测试
python test_api.py
```

测试脚本将验证：
- 健康检查端点
- 基本 tokenization 功能
- 缓存机制
- 不同模型支持
- 错误处理

## 性能优化

1. **缓存机制**: 首次加载的 tokenizer 会被缓存，后续请求直接使用缓存
2. **异步处理**: 使用异步 I/O 提高并发性能
3. **线程池**: CPU 密集型的 tokenization 操作在线程池中执行

## 错误处理

服务提供详细的错误信息：

- `400 Bad Request`: 缺少必需参数
- `500 Internal Server Error`: 模型加载失败或 tokenization 错误

## 日志

服务会记录详细的日志信息，包括：
- 模型加载状态
- 缓存使用情况
- 错误信息

## 部署建议

### Docker 部署

可以创建 Dockerfile 进行容器化部署：

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 生产环境

生产环境建议：
- 使用 Gunicorn + Uvicorn workers
- 配置反向代理 (Nginx)
- 启用日志轮转
- 设置适当的缓存策略

## 许可证

本项目基于 MIT 许可证开源。 # llm-tokenizer
