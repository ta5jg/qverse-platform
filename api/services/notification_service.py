from __future__ import annotations

from datetime import datetime, timezone


class NotificationService:
    def health(self):
        return {
            "healthy": True,
            "service": "notification_service",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def metrics(self):
        return {
            "service": "notification_service",
            "healthy": True,
        }


notification_service = NotificationService()
