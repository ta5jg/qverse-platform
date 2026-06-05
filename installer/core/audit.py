from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List


class AuditEngine:
    def __init__(self) -> None:
        self.events: List[Dict[str, Any]] = []

    def record(self, action: str, actor: str = "system") -> Dict[str, Any]:
        event = {
            "action": action,
            "actor": actor,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.events.append(event)
        return event

    def health(self) -> Dict[str, Any]:
        return {
            "healthy": True,
            "engine": "audit",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def summary(self) -> Dict[str, Any]:
        return {
            "engine": "audit",
            "status": "ready",
            "events": len(self.events),
        }


audit_engine = AuditEngine()
