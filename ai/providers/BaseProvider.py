class BaseProvider:
    name = "base"

    def __init__(self, config=None):
        self.config = config or {}

    def env_key(self):
        return self.config.get("env_key", "")

    def api_key(self):
        import os
        return os.getenv(self.env_key(), "")

    def available(self):
        return True

    def transport_enabled(self):
        if self.name == "ollama":
            return True
        return bool(self.api_key())

    def generate(self, prompt: str, context=None):
        return {
            "provider": self.name,
            "status": "ready",
            "transport_enabled": self.transport_enabled(),
            "prompt": prompt,
            "context": context or {},
            "response": f"{self.name} transport layer initialized",
        }
