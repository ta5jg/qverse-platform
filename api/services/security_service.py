from __future__ import annotations

from datetime import datetime, timezone


class SecurityService:
    def health(self):
        return {
            "healthy": True,
            "service": "security_service",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def metrics(self):
        return {
            "service": "security_service",
            "healthy": True,
        }


security_service = SecurityService()
