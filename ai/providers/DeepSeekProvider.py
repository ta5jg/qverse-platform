from ai.providers.BaseProvider import BaseProvider


class DeepSeekProvider(BaseProvider):
    name = "deepseek"

    def __init__(self, config=None):
        config = config or {}
        config["env_key"] = "DEEPSEEK_API_KEY"
        super().__init__(config=config)
