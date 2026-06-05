from __future__ import annotations

from datetime import datetime, timezone


class ModelService:
    def health(self):
        return {
            "healthy": True,
            "service": "model_service",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def metrics(self):
        return {
            "service": "model_service",
            "healthy": True,
        }


model_service = ModelService()
