from ai.providers.BaseProvider import BaseProvider


class OllamaProvider(BaseProvider):
    name = "ollama"

    def __init__(self, config=None):
        config = config or {}
        config["env_key"] = "OLLAMA_BASE_URL"
        super().__init__(config=config)
