from __future__ import annotations

from datetime import datetime, timezone


class RuntimeService:
    def health(self):
        return {
            "healthy": True,
            "service": "runtime_service",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def metrics(self):
        return {
            "service": "runtime_service",
            "healthy": True,
        }


runtime_service = RuntimeService()
