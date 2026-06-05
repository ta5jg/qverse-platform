from __future__ import annotations

from datetime import datetime, timezone


class HealthService:
    def health(self):
        return {
            "healthy": True,
            "service": "health_service",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def metrics(self):
        return {
            "service": "health_service",
            "healthy": True,
        }


health_service = HealthService()
