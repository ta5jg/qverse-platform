from ai.router.ModelRouter import ModelRouter


class AIResponseEngine:
    def __init__(self):
        self.router = ModelRouter()

    def respond(self, prompt: str, context=None, provider=None):
        result = self.router.generate(prompt=prompt, context=context or {}, provider=provider)
        return {
            "engine": "ai_response_engine",
            "version": "V9",
            "result": result,
        }
