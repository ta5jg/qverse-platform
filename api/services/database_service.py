from __future__ import annotations

from datetime import datetime, timezone


class DatabaseService:
    def health(self):
        return {
            "healthy": True,
            "service": "database_service",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def metrics(self):
        return {
            "service": "database_service",
            "healthy": True,
        }


database_service = DatabaseService()
