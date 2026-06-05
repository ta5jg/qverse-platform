from __future__ import annotations

from api.services.project_service import project_service


class ProjectManager:
    def health(self):
        return {
            "healthy": True,
            "manager": "project_manager",
        }

    def metrics(self):
        return {
            "manager": "project_manager",
            **project_service.metrics(),
        }


project_manager = ProjectManager()
