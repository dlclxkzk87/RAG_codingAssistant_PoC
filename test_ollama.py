import requests

url = "http://localhost:11434/api/generate"

payload = {
    "model": "qwen2.5-coder:7b",
    "prompt": "python 리스트와 튜플 차이를 예제로 설명해줘",
    "stream": False
}

response = requests.post(url, json=payload)
print(response.json()["response"])
