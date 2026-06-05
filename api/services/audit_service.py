from __future__ import annotations

from datetime import datetime, timezone


class AuditService:
    def health(self):
        return {
            "healthy": True,
            "service": "audit_service",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def metrics(self):
        return {
            "service": "audit_service",
            "healthy": True,
        }


audit_service = AuditService()
