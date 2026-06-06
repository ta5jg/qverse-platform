class ProviderHealthMonitor:
    PROVIDERS = ["openai", "claude", "gemini", "deepseek", "qwen"]

    def __init__(self):
        # In a real system, configuration and health checks would be loaded here.
        pass

    def build_status(self):
        status = {}
        for name in self.PROVIDERS:
            # Placeholder: In reality, count and health would be determined dynamically.
            status[name] = {
                "configured_count": 1,
                "healthy": True
            }
        return status
