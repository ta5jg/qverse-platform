import os
import requests

class DeepSeekProvider:
    def __init__(self):
        self.api_key = os.environ.get("DEEPSEEK_API_KEY")
        self.model = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
        self.api_url = "https://api.deepseek.com/chat/completions"

    def chat(self, prompt, context=None):
        if not self.api_key:
            return {
                "provider": "deepseek",
                "transport_enabled": False,
                "error": "DEEPSEEK_API_KEY not set"
            }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "content-type": "application/json"
        }
        messages = []
        if context:
            messages.append({"role": "system", "content": context})
        messages.append({"role": "user", "content": prompt})
        data = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 1024
        }
        try:
            resp = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            resp.raise_for_status()
            out = resp.json()
            return {
                "provider": "deepseek",
                "transport_enabled": True,
                "response": out.get("choices", out)
            }
        except Exception as e:
            return {
                "provider": "deepseek",
                "transport_enabled": False,
                "error": str(e)
            }
