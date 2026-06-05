from __future__ import annotations

from api.services.integration_service import integration_service


class IntegrationManager:
    def health(self):
        return {
            "healthy": True,
            "manager": "integration_manager",
        }

    def metrics(self):
        return {
            "manager": "integration_manager",
            **integration_service.metrics(),
        }


integration_manager = IntegrationManager()
