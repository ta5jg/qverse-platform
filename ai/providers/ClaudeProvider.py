import os
import requests

class ClaudeProvider:
    def __init__(self):
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.model = os.environ.get("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest")
        self.api_url = "https://api.anthropic.com/v1/messages"

    def chat(self, prompt, context=None):
        if not self.api_key:
            return {
                "provider": "claude",
                "transport_enabled": False,
                "error": "ANTHROPIC_API_KEY not set"
            }
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1024
        }
        if context:
            data["messages"].insert(0, {"role": "system", "content": context})
        try:
            resp = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            resp.raise_for_status()
            out = resp.json()
            return {
                "provider": "claude",
                "transport_enabled": True,
                "response": out.get("content", out)
            }
        except Exception as e:
            return {
                "provider": "claude",
                "transport_enabled": False,
                "error": str(e)
            }
