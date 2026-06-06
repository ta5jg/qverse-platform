import os
import requests

class OpenAIProvider:
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    def chat(self, prompt, context=None):
        if not self.api_key:
            return {
                "provider": "openai",
                "transport_enabled": False,
                "response": None
            }
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": context or ""},
                {"role": "user", "content": prompt}
            ]
        }
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            assistant_text = (
                data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", None)
            )
            return {
                "provider": "openai",
                "transport_enabled": True,
                "response": assistant_text
            }
        except Exception as e:
            return {
                "provider": "openai",
                "transport_enabled": False,
                "response": f"error: {str(e)}"
            }
