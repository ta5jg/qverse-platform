import os
import requests

from memory.storage.SecretStore import secret_store


class AIResponseEngine:
    def __init__(self):
        self.provider = "openai"
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def _get_openai_key(self):
        return os.getenv("OPENAI_API_KEY") or secret_store.get_secret("OPENAI_API_KEY")

    def respond(self, prompt, context=None):
        api_key = self._get_openai_key()
        if not api_key:
            return {
                "engine": "ai_response_engine",
                "version": "V12",
                "result": {
                    "provider": "openai",
                    "status": "missing_api_key",
                    "transport_enabled": False,
                    "prompt": prompt,
                    "context": context or {},
                    "response": None,
                    "fallback_used": True,
                },
            }

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are Q-Verse Agent, a concise and helpful AI runtime assistant.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.4,
                },
                timeout=45,
            )
            response.raise_for_status()
            data = response.json()
            text = data["choices"][0]["message"]["content"]
            return {
                "engine": "ai_response_engine",
                "version": "V12",
                "result": {
                    "provider": "openai",
                    "status": "completed",
                    "transport_enabled": True,
                    "prompt": prompt,
                    "context": context or {},
                    "response": text,
                    "fallback_used": False,
                },
            }
        except Exception as exc:
            return {
                "engine": "ai_response_engine",
                "version": "V12",
                "result": {
                    "provider": "openai",
                    "status": "error",
                    "transport_enabled": True,
                    "prompt": prompt,
                    "context": context or {},
                    "error": exc.__class__.__name__,
                    "message": str(exc),
                    "response": None,
                    "fallback_used": True,
                },
            }

    def chat(self, prompt, context=None):
        return self.respond(prompt, context)

    def generate(self, prompt, context=None):
        return self.respond(prompt, context)


ai_response_engine = AIResponseEngine()
