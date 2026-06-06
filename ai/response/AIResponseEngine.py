from ai.router.ProviderSelector import ProviderSelector
from ai.providers.OpenAIProvider import OpenAIProvider
from ai.providers.ClaudeProvider import ClaudeProvider
from ai.providers.GeminiProvider import GeminiProvider
from ai.providers.DeepSeekProvider import DeepSeekProvider
from ai.providers.QwenProvider import QwenProvider

class AIResponseEngine:
    def __init__(self):
        self.selector = ProviderSelector()
        self.providers = {
            "openai": OpenAIProvider(),
            "claude": ClaudeProvider(),
            "gemini": GeminiProvider(),
            "deepseek": DeepSeekProvider(),
            "qwen": QwenProvider()
        }

    def chat(self, prompt, context=None):
        for name in self.selector.select_order():
            provider = self.providers.get(name)
            if not provider or not getattr(provider, "transport_enabled", True):
                continue
            try:
                result = provider.chat(prompt, context)
                if result:
                    return {
                        "engine": "ai_response_engine",
                        "version": "V10.4",
                        "result": result
                    }
            except Exception:
                continue
        return {
            "engine": "ai_response_engine",
            "version": "V10.4",
            "result": None
        }
