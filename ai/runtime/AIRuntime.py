from ai.response.AIResponseEngine import AIResponseEngine


class AIRuntime:
    def __init__(self):
        self.response_engine = AIResponseEngine()

    def status(self):
        return {
            "status": "running",
            "version": "V9",
            "enterprise": True,
            "transport": "enabled_when_env_present",
            "routing": "multi_provider_enterprise",
            "providers": [
                "openai",
                "anthropic",
                "gemini",
                "deepseek",
                "qwen",
                "ollama",
            ],
        }

    def generate(self, prompt: str, context=None, provider=None):
        return self.response_engine.respond(prompt=prompt, context=context or {}, provider=provider)


def runtime_status():
    return AIRuntime().status()


def generate_ai_response(prompt: str, context=None, provider=None):
    return AIRuntime().generate(prompt=prompt, context=context or {}, provider=provider)
