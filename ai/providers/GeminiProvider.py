from ai.providers.BaseProvider import BaseProvider


class GeminiProvider(BaseProvider):
    name = "gemini"

    def __init__(self, config=None):
        config = config or {}
        config["env_key"] = "GEMINI_API_KEY"
        super().__init__(config=config)
