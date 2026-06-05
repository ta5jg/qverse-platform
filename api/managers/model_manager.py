from __future__ import annotations

from api.services.model_service import model_service


class ModelManager:
    def health(self):
        return {
            "healthy": True,
            "manager": "model_manager",
        }

    def metrics(self):
        return {
            "manager": "model_manager",
            **model_service.metrics(),
        }


model_manager = ModelManager()
