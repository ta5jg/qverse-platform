from __future__ import annotations

from datetime import datetime, timezone


class MarketplaceService:
    def health(self):
        return {
            "healthy": True,
            "service": "marketplace_service",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def metrics(self):
        return {
            "service": "marketplace_service",
            "healthy": True,
        }


marketplace_service = MarketplaceService()
