from ai.providers.OpenAIProvider import OpenAIProvider
from ai.providers.ClaudeProvider import ClaudeProvider
from ai.providers.GeminiProvider import GeminiProvider
from ai.providers.DeepSeekProvider import DeepSeekProvider
from ai.providers.QwenProvider import QwenProvider
from ai.providers.OllamaProvider import OllamaProvider
from ai.router.ProviderSelector import ProviderSelector
from ai.router.FallbackEngine import FallbackEngine


class ModelRouter:
    def __init__(self):
        self.selector = ProviderSelector()
        self.fallback = FallbackEngine()
        self.providers = {
            "openai": OpenAIProvider(),
            "anthropic": ClaudeProvider(),
            "gemini": GeminiProvider(),
            "deepseek": DeepSeekProvider(),
            "qwen": QwenProvider(),
            "ollama": OllamaProvider(),
        }

    def status(self):
        return {
            "status": "ready",
            "provider_count": len(self.providers),
            "providers": list(self.providers.keys()),
            "routing": "multi_provider_enterprise",
        }

    def generate(self, prompt: str, context=None, provider=None):
        selected = self.selector.select(provider)
        ordered_names = [selected] + [name for name in self.selector.fallback_order() if name != selected]
        ordered_providers = [self.providers[name] for name in ordered_names if name in self.providers]
        return self.fallback.run_with_fallback(ordered_providers, prompt, context or {})
