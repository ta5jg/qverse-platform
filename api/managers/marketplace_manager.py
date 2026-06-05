from __future__ import annotations

from api.services.marketplace_service import marketplace_service


class MarketplaceManager:
    def health(self):
        return {
            "healthy": True,
            "manager": "marketplace_manager",
        }

    def metrics(self):
        return {
            "manager": "marketplace_manager",
            **marketplace_service.metrics(),
        }


marketplace_manager = MarketplaceManager()
