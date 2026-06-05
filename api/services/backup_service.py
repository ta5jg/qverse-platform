from __future__ import annotations

from datetime import datetime, timezone


class BackupService:
    def health(self):
        return {
            "healthy": True,
            "service": "backup_service",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def metrics(self):
        return {
            "service": "backup_service",
            "healthy": True,
        }


backup_service = BackupService()
