from __future__ import annotations

from datetime import datetime, timezone


class WorkflowService:
    def health(self):
        return {
            "healthy": True,
            "service": "workflow_service",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def metrics(self):
        return {
            "service": "workflow_service",
            "healthy": True,
        }


workflow_service = WorkflowService()
