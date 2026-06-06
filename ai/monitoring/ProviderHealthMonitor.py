import os


class ProviderHealthMonitor:
    KEYS = {
        "openai": "OPENAI_API_KEY",
        "claude": "ANTHROPIC_API_KEY",
        "gemini": "GEMINI_API_KEY",
        "deepseek": "DEEPSEEK_API_KEY",
        "qwen": "QWEN_API_KEY",
    }

    def build_status(self):
        providers = {
            provider: {"configured": bool(os.getenv(env_key)), "env_key": env_key}
            for provider, env_key in self.KEYS.items()
        }
        configured_count = sum(1 for item in providers.values() if item["configured"])
        return {
            "providers": providers,
            "configured_count": configured_count,
            "healthy": configured_count > 0,
        }


provider_health_monitor = ProviderHealthMonitor()
