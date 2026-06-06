import os
from memory.storage.SecretStore import secret_store


class ProviderAdmin:
    PROVIDER_KEYS = {
        "openai": "OPENAI_API_KEY",
        "claude": "ANTHROPIC_API_KEY",
        "gemini": "GEMINI_API_KEY",
        "deepseek": "DEEPSEEK_API_KEY",
        "qwen": "QWEN_API_KEY",
    }

    def save_provider_key(self, provider, api_key):
        env_key = self.PROVIDER_KEYS.get(provider)
        if not env_key:
            return {"success": False, "error": "unsupported_provider", "provider": provider}
        saved = secret_store.save_secret(env_key, api_key)
        return {"success": True, "provider": provider, "env_key": env_key, "secret": saved}

    def list_providers(self):
        secrets = secret_store.list_secrets()
        providers = {}
        for provider, env_key in self.PROVIDER_KEYS.items():
            stored = secrets.get(env_key, {})
            providers[provider] = {
                "env_key": env_key,
                "configured": bool(os.getenv(env_key)) or stored.get("configured", False),
                "masked": stored.get("masked", ""),
            }
        return providers


provider_admin = ProviderAdmin()
