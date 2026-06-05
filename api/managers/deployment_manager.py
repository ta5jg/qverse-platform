from __future__ import annotations

from api.services.deployment_service import deployment_service


class DeploymentManager:
    def health(self):
        return {
            "healthy": True,
            "manager": "deployment_manager",
        }

    def metrics(self):
        return {
            "manager": "deployment_manager",
            **deployment_service.metrics(),
        }


deployment_manager = DeploymentManager()
