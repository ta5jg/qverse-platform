from __future__ import annotations

from api.services.agent_service import agent_service


class AgentManager:
    def health(self):
        return {
            "healthy": True,
            "manager": "agent_manager",
        }

    def metrics(self):
        return {
            "manager": "agent_manager",
            **agent_service.metrics(),
        }


agent_manager = AgentManager()
