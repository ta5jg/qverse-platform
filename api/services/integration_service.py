from __future__ import annotations

from datetime import datetime, timezone


class IntegrationService:
    def health(self):
        return {
            "healthy": True,
            "service": "integration_service",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def metrics(self):
        return {
            "service": "integration_service",
            "healthy": True,
        }


integration_service = IntegrationService()
