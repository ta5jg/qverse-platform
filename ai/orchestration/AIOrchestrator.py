from ai.runtime.AIRuntime import generate_ai_response


class AIOrchestrator:
    def status(self):
        return "active"

    def run(self, prompt: str, context=None, provider=None):
        return generate_ai_response(prompt=prompt, context=context or {}, provider=provider)
