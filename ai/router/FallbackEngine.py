class FallbackEngine:
    def run_with_fallback(self, providers, prompt: str, context=None):
        errors = []
        for provider in providers:
            try:
                if provider.available():
                    result = provider.generate(prompt, context or {})
                    result["fallback_used"] = len(errors) > 0
                    return result
            except Exception as exc:
                errors.append({"provider": provider.name, "error": str(exc)})
        return {
            "status": "failed",
            "errors": errors,
            "response": "No AI provider was available.",
        }
