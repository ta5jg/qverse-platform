from ai.providers.BaseProvider import BaseProvider


class ClaudeProvider(BaseProvider):
    name = "anthropic"

    def __init__(self, config=None):
        config = config or {}
        config["env_key"] = "ANTHROPIC_API_KEY"
        super().__init__(config=config)
