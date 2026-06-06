import os
import requests

from memory.storage.SecretStore import secret_store


class AIResponseEngine:
    PROVIDER_ORDER = ["openai", "gemini", "deepseek", "qwen"]

    PROVIDER_KEYS = {
        "openai": "OPENAI_API_KEY",
        "gemini": "GEMINI_API_KEY",
        "deepseek": "DEEPSEEK_API_KEY",
        "qwen": "QWEN_API_KEY",
    }

    DEFAULT_MODELS = {
        "openai": "gpt-4o-mini",
        "gemini": "gemini-1.5-flash",
        "deepseek": "deepseek-chat",
        "qwen": "qwen-turbo",
    }

    def __init__(self):
        self.provider = os.getenv("QVERSE_DEFAULT_PROVIDER", "openai")
        self.model = os.getenv("OPENAI_MODEL", self.DEFAULT_MODELS["openai"])

    def _get_key(self, provider):
        env_key = self.PROVIDER_KEYS.get(provider)
        if not env_key:
            return None
        return os.getenv(env_key) or secret_store.get_secret(env_key)

    def _system_prompt(self, provider):
        return (
            "You are Q-Verse Agent, the live AI runtime of the Q-Verse Platform. "
            f"You are currently connected through the configured {provider} provider. "
            "When transport_enabled is true, you must answer as the live Q-Verse runtime. "
            "Do not claim you are offline, static, not connected, unable to answer live, or only a pre-trained assistant. "
            "If the user asks whether Q-Verse is connected to an AI provider, answer yes and explain briefly which configured provider produced the response. "
            "Answer in the user's language. Be concise, direct, and helpful."
        )

    def _provider_sequence(self, provider=None):
        requested = provider or self.provider or "openai"
        sequence = []
        if requested in self.PROVIDER_ORDER:
            sequence.append(requested)
        for item in self.PROVIDER_ORDER:
            if item not in sequence:
                sequence.append(item)
        return sequence

    def _model_for(self, provider, model=None):
        if model:
            return model
        if provider == "openai":
            return os.getenv("OPENAI_MODEL", self.DEFAULT_MODELS[provider])
        if provider == "gemini":
            return os.getenv("GEMINI_MODEL", self.DEFAULT_MODELS[provider])
        if provider == "deepseek":
            return os.getenv("DEEPSEEK_MODEL", self.DEFAULT_MODELS[provider])
        if provider == "qwen":
            return os.getenv("QWEN_MODEL", self.DEFAULT_MODELS[provider])
        return self.DEFAULT_MODELS.get(provider, self.model)

    def _chat_openai_compatible(self, provider, prompt, context=None, model=None):
        api_key = self._get_key(provider)
        if not api_key:
            raise RuntimeError(f"missing_api_key:{provider}")

        base_urls = {
            "openai": "https://api.openai.com/v1/chat/completions",
            "deepseek": "https://api.deepseek.com/chat/completions",
            "qwen": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        }
        url = base_urls[provider]
        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self._model_for(provider, model),
                "messages": [
                    {"role": "system", "content": self._system_prompt(provider)},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.4,
            },
            timeout=45,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    def _chat_gemini(self, prompt, context=None, model=None):
        provider = "gemini"
        api_key = self._get_key(provider)
        if not api_key:
            raise RuntimeError("missing_api_key:gemini")

        gemini_model = self._model_for(provider, model)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{gemini_model}:generateContent?key={api_key}"
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json={
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {"text": self._system_prompt(provider) + "\n\nUser: " + prompt}
                        ],
                    }
                ],
                "generationConfig": {"temperature": 0.4},
            },
            timeout=45,
        )
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

    def _try_provider(self, provider, prompt, context=None, model=None):
        if provider == "gemini":
            return self._chat_gemini(prompt, context=context, model=model)
        if provider in {"openai", "deepseek", "qwen"}:
            return self._chat_openai_compatible(provider, prompt, context=context, model=model)
        raise RuntimeError(f"unsupported_provider:{provider}")

    def respond(self, prompt, context=None, provider=None, model=None, **kwargs):
        attempts = []
        for candidate in self._provider_sequence(provider):
            try:
                text = self._try_provider(candidate, prompt, context=context, model=model)
                return {
                    "engine": "ai_response_engine",
                    "version": "V12.2",
                    "result": {
                        "provider": candidate,
                        "status": "completed",
                        "transport_enabled": True,
                        "prompt": prompt,
                        "context": context or {},
                        "response": text,
                        "fallback_used": candidate != (provider or self.provider or "openai"),
                        "attempts": attempts,
                    },
                }
            except Exception as exc:
                attempts.append({
                    "provider": candidate,
                    "error": exc.__class__.__name__,
                    "message": str(exc),
                })
                continue

        return {
            "engine": "ai_response_engine",
            "version": "V12.2",
            "result": {
                "provider": provider or self.provider or "openai",
                "status": "error",
                "transport_enabled": True,
                "prompt": prompt,
                "context": context or {},
                "response": None,
                "fallback_used": True,
                "attempts": attempts,
            },
        }

    def chat(self, prompt, context=None, provider=None, model=None, **kwargs):
        return self.respond(prompt, context=context, provider=provider, model=model, **kwargs)

    def generate(self, prompt, context=None, provider=None, model=None, **kwargs):
        return self.respond(prompt, context=context, provider=provider, model=model, **kwargs)


ai_response_engine = AIResponseEngine()
