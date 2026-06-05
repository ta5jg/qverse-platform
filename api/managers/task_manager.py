from __future__ import annotations

from api.services.task_service import task_service


class TaskManager:
    def health(self):
        return {
            "healthy": True,
            "manager": "task_manager",
        }

    def metrics(self):
        return {
            "manager": "task_manager",
            **task_service.metrics(),
        }


task_manager = TaskManager()
