from __future__ import annotations

from api.services.workflow_service import workflow_service


class WorkflowManager:
    def health(self):
        return {
            "healthy": True,
            "manager": "workflow_manager",
        }

    def metrics(self):
        return {
            "manager": "workflow_manager",
            **workflow_service.metrics(),
        }


workflow_manager = WorkflowManager()
