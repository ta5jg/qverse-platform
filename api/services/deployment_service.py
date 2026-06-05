from __future__ import annotations

from datetime import datetime, timezone


class DeploymentService:
    def health(self):
        return {
            "healthy": True,
            "service": "deployment_service",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def metrics(self):
        return {
            "service": "deployment_service",
            "healthy": True,
        }


deployment_service = DeploymentService()
