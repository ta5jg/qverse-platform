from __future__ import annotations

from datetime import datetime, timezone


class SystemService:
    def health(self):
        return {
            "healthy": True,
            "service": "system_service",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def metrics(self):
        return {
            "service": "system_service",
            "healthy": True,
        }


system_service = SystemService()
