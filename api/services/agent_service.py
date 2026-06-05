from __future__ import annotations

from datetime import datetime, timezone


class AgentService:
    def health(self):
        return {
            "healthy": True,
            "service": "agent_service",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def metrics(self):
        return {
            "service": "agent_service",
            "healthy": True,
        }


agent_service = AgentService()
