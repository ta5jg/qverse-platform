from __future__ import annotations

from datetime import datetime, timezone


class TaskService:
    def health(self):
        return {
            "healthy": True,
            "service": "task_service",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def metrics(self):
        return {
            "service": "task_service",
            "healthy": True,
        }


task_service = TaskService()
