SUPPORTED_MODELS = [
    "openai",
    "anthropic",
    "gemini",
    "ollama",
    "deepseek",
]


def list_supported_models() -> list[str]:
    return SUPPORTED_MODELS.copy()
