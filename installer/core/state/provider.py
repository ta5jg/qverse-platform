"""Provider Readiness Engine"""



def evaluate_ai_readiness(self, state: SystemState) -> AIReadiness:
        providers = state.models.copy()

        score = 0
        for enabled in providers.values():
            if enabled:
                score += 10

        score = min(score, 100)

        return AIReadiness(
            score=score,
            providers=providers,
        )

def evaluate_provider_readiness(self, state: SystemState) -> ProviderReadiness:
        available = [k for k, v in state.models.items() if v]

        return ProviderReadiness(
            score=min(100, len(available) * 10),
            available=available,
        )