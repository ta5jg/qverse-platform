from ai.models.ModelRegistry import DEFAULT_PROVIDER_ORDER


class ProviderSelector:
    def select(self, requested_provider=None):
        if requested_provider:
            return requested_provider
        return DEFAULT_PROVIDER_ORDER[0]

    def fallback_order(self):
        return list(DEFAULT_PROVIDER_ORDER)
