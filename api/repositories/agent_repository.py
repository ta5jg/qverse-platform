from __future__ import annotations

from typing import Any, Dict, List, Optional

from api.repositories.base_repository import BaseRepository


class AgentRepository(BaseRepository[Dict[str, Any]]):
    def find_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        for item in self.list_all():
            if item.get("name") == name:
                return item
        return None

    def metrics(self) -> Dict[str, Any]:
        return {
            "repository": "agent_repository",
            "total_records": self.count(),
        }


agent_repository = AgentRepository()
