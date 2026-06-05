from __future__ import annotations

from datetime import datetime, timezone


class ConfigService:
    def health(self):
        return {
            "healthy": True,
            "service": "config_service",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def metrics(self):
        return {
            "service": "config_service",
            "healthy": True,
        }


config_service = ConfigService()
