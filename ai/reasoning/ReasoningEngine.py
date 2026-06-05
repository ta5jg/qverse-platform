class ReasoningEngine:
    def status(self):
        return "ready"

    def reason(self, prompt: str):
        return {
            "prompt": prompt,
            "reasoning_mode": "structured",
            "status": "ready",
        }
