from __future__ import annotations

from api.services.notification_service import notification_service


class NotificationManager:
    def health(self):
        return {
            "healthy": True,
            "manager": "notification_manager",
        }

    def metrics(self):
        return {
            "manager": "notification_manager",
            **notification_service.metrics(),
        }


notification_manager = NotificationManager()
