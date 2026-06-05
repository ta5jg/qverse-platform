from __future__ import annotations

from datetime import datetime, timezone


class ProjectService:
    def health(self):
        return {
            "healthy": True,
            "service": "project_service",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def metrics(self):
        return {
            "service": "project_service",
            "healthy": True,
        }


project_service = ProjectService()
