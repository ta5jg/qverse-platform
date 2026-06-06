import os
import requests

class QwenProvider:
    def __init__(self):
        self.api_key = os.environ.get("QWEN_API_KEY")
        self.model = os.environ.get("QWEN_MODEL", "qwen-plus")
        self.base_url = os.environ.get("QWEN_BASE_URL", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions")

    def chat(self, prompt, context=None):
        if not self.api_key:
            return {
                "provider": "qwen",
                "transport_enabled": False,
                "error": "QWEN_API_KEY not set"
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
            resp = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            resp.raise_for_status()
            out = resp.json()
            return {
                "provider": "qwen",
                "transport_enabled": True,
                "response": out.get("choices", out)
            }
        except Exception as e:
            return {
                "provider": "qwen",
                "transport_enabled": False,
                "error": str(e)
            }
