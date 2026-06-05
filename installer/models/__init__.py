"""Q-Verse Installer Model Providers V9."""

MODEL_PROVIDERS = [
    "anthropic",
    "deepseek",
    "gemini",
    "lmstudio",
    "ollama",
    "openai",
    "openrouter",
]


def list_model_providers() -> list[str]:
    return MODEL_PROVIDERS.copy()
