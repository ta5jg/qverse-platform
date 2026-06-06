class ProviderSelector:
    SUPPORTED_PROVIDERS = ["openai", "claude", "gemini", "deepseek", "qwen"]

    def __init__(self):
        from os import environ
        self.default = environ.get("AI_DEFAULT_PROVIDER", "openai")
        self.fallback = environ.get("AI_FALLBACK_PROVIDER", "claude")

    def select_order(self):
        order = []
        used = set()
        if self.default in self.SUPPORTED_PROVIDERS:
            order.append(self.default)
            used.add(self.default)
        if self.fallback in self.SUPPORTED_PROVIDERS and self.fallback not in used:
            order.append(self.fallback)
            used.add(self.fallback)
        for p in self.SUPPORTED_PROVIDERS:
            if p not in used:
                order.append(p)
        return order
