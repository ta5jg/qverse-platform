from __future__ import annotations

from typing import Any, Dict, List, Optional

from api.repositories.base_repository import BaseRepository


class AuditRepository(BaseRepository[Dict[str, Any]]):
    def find_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        for item in self.list_all():
            if item.get("name") == name:
                return item
        return None

    def metrics(self) -> Dict[str, Any]:
        return {
            "repository": "audit_repository",
            "total_records": self.count(),
        }


audit_repository = AuditRepository()
