from ai.providers.BaseProvider import BaseProvider


class OpenAIProvider(BaseProvider):
    name = "openai"

    def __init__(self, config=None):
        config = config or {}
        config["env_key"] = "OPENAI_API_KEY"
        super().__init__(config=config)
