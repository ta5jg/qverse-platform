from ai.providers.BaseProvider import BaseProvider


class QwenProvider(BaseProvider):
    name = "qwen"

    def __init__(self, config=None):
        config = config or {}
        config["env_key"] = "QWEN_API_KEY"
        super().__init__(config=config)
