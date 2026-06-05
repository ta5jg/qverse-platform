

from datetime import datetime, timezone
from typing import Any, Dict, Generic, List, Optional, TypeVar


T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Generic in-memory repository base implementation."""

    def __init__(self) -> None:
        self._items: Dict[str, T] = {}
        self.created_at = datetime.now(timezone.utc).isoformat()

    def create(self, entity_id: str, entity: T) -> T:
        self._items[entity_id] = entity
        return entity

    def get(self, entity_id: str) -> Optional[T]:
        return self._items.get(entity_id)

    def update(self, entity_id: str, entity: T) -> Optional[T]:
        if entity_id not in self._items:
            return None

        self._items[entity_id] = entity
        return entity

    def delete(self, entity_id: str) -> bool:
        return self._items.pop(entity_id, None) is not None

    def exists(self, entity_id: str) -> bool:
        return entity_id in self._items

    def list_all(self) -> List[T]:
        return list(self._items.values())

    def count(self) -> int:
        return len(self._items)

    def clear(self) -> None:
        self._items.clear()

    def metadata(self) -> Dict[str, Any]:
        return {
            "repository": self.__class__.__name__,
            "created_at": self.created_at,
            "total_items": self.count(),
        }