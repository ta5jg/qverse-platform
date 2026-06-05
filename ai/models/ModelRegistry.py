MODELS = {
    "openai": ["gpt-4o", "gpt-5"],
    "anthropic": ["claude-sonnet", "claude-opus"],
    "gemini": ["gemini-pro", "gemini-flash"],
    "deepseek": ["deepseek-chat", "deepseek-reasoner"],
    "qwen": ["qwen-max", "qwen-plus"],
    "ollama": ["llama", "mistral", "qwen"],
    "openrouter": ["auto", "router-best"],
    "groq": ["llama", "mixtral"],
    "together": ["llama", "mistral", "qwen"],
    "azure_openai": ["gpt-4o", "gpt-5"],
}

DEFAULT_PROVIDER_ORDER = [
    "openai",
    "anthropic",
    "gemini",
    "deepseek",
    "qwen",
    "openrouter",
    "ollama",
]
