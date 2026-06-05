from __future__ import annotations

from api.services.system_service import system_service


class SystemManager:
    def health(self):
        return {
            "healthy": True,
            "manager": "system_manager",
        }

    def metrics(self):
        return {
            "manager": "system_manager",
            **system_service.metrics(),
        }


system_manager = SystemManager()
