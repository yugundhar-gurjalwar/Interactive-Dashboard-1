import requests
import json

base_url = "http://localhost:8000/api/v1"

print("1. Testing /models to confirm llama3...")
try:
    resp = requests.get(f"{base_url}/models/")
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text}")
except Exception as e:
    print(f"Models failed: {e}")

print("\n2. Testing /chat/completions with llama3...")
data = {
    "messages": [{"role": "user", "content": "Say hello in one word."}],
    "model": "llama3",
    "stream": False
}
try:
    # Authenticate as guest first
    auth_resp = requests.post(f"{base_url}/auth/login/guest")
    token = auth_resp.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    resp = requests.post(f"{base_url}/chat/completions", json=data, headers=headers)
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text}")
except Exception as e:
    print(f"Chat failed: {e}")
