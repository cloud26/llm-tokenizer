import time

import requests

# API 基础 URL
BASE_URL = "http://localhost:8000"


def test_health_check():
    """测试健康检查端点"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check response: {response.json()}")
    return response.status_code == 200


def test_tokenization():
    """测试 tokenization 功能"""
    print("\nTesting tokenization...")

    # 测试数据
    test_data = {
        "text": "Hello, how are you today?",
        "hubPath": "bert-base-uncased"
    }

    print(f"Request data: {test_data}")

    # 发送请求
    start_time = time.time()
    response = requests.post(
        f"{BASE_URL}/tokenize",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    end_time = time.time()

    print(f"Response status: {response.status_code}")
    print(f"Response time: {end_time - start_time:.2f} seconds")

    if response.status_code == 200:
        result = response.json()
        print("Tokenization result:")
        print(f"  Success: {result['success']}")
        print(f"  Token count: {result['tokenCount']}")
        print(f"  Tokens: {result['tokens']}")
        print(f"  Token IDs: {result['tokenIds']}")
        return True
    else:
        print(f"Error: {response.text}")
        return False


def test_cache_functionality():
    """测试缓存功能"""
    print("\nTesting cache functionality...")

    # 获取缓存信息
    response = requests.get(f"{BASE_URL}/cache")
    if response.status_code == 200:
        cache_info = response.json()
        print(f"Cache info: {cache_info}")

    # 测试相同的 tokenizer（应该使用缓存）
    test_data = {
        "text": "This is a second test.",
        "hubPath": "bert-base-uncased"
    }

    start_time = time.time()
    response = requests.post(
        f"{BASE_URL}/tokenize",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    end_time = time.time()

    print(f"Second request (cached) time: {end_time - start_time:.2f} seconds")

    return response.status_code == 200


def test_different_models():
    """测试不同的模型"""
    print("\nTesting different models...")

    models_to_test = [
        "gpt2",
        "distilbert-base-uncased"
    ]

    for model in models_to_test:
        print(f"\nTesting model: {model}")
        test_data = {
            "text": "Testing different tokenizer models.",
            "hubPath": model
        }

        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/tokenize",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        end_time = time.time()

        print(
            f"Response time for {model}: {end_time - start_time:.2f} seconds")

        if response.status_code == 200:
            result = response.json()
            print(f"Token count: {result['tokenCount']}")
            print(f"First 5 tokens: {result['tokens'][:5]}")
        else:
            print(f"Error with {model}: {response.text}")


def test_error_handling():
    """测试错误处理"""
    print("\nTesting error handling...")

    # 测试缺少参数
    test_data = {"text": "Hello"}  # 缺少 hubPath
    response = requests.post(
        f"{BASE_URL}/tokenize",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Missing hubPath response: {response.status_code}")

    # 测试无效的模型
    test_data = {
        "text": "Hello",
        "hubPath": "invalid-model-name"
    }
    response = requests.post(
        f"{BASE_URL}/tokenize",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Invalid model response: {response.status_code}")


if __name__ == "__main__":
    print("Starting API tests...")
    print("Make sure the FastAPI server is running on http://localhost:8000")
    print("=" * 50)

    try:
        # 运行所有测试
        test_health_check()
        test_tokenization()
        test_cache_functionality()
        test_different_models()
        test_error_handling()

        print("\n" + "=" * 50)
        print("All tests completed!")

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Please make sure the server is running with: python main.py")
    except Exception as e:
        print(f"Test failed with error: {e}")
