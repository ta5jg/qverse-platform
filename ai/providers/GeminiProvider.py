import os
import requests

class GeminiProvider:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.model = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"

    def chat(self, prompt, context=None):
        if not self.api_key:
            return {
                "provider": "gemini",
                "transport_enabled": False,
                "error": "GEMINI_API_KEY not set"
            }
        headers = {
            "content-type": "application/json"
        }
        data = {
            "contents": [
                {"role": "user", "parts": [{"text": prompt}]}
            ]
        }
        if context:
            data["contents"].insert(0, {"role": "system", "parts": [{"text": context}]})
        params = {"key": self.api_key}
        try:
            resp = requests.post(self.api_url, headers=headers, params=params, json=data, timeout=30)
            resp.raise_for_status()
            out = resp.json()
            return {
                "provider": "gemini",
                "transport_enabled": True,
                "response": out.get("candidates", out)
            }
        except Exception as e:
            return {
                "provider": "gemini",
                "transport_enabled": False,
                "error": str(e)
            }
