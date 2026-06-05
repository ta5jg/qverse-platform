from __future__ import annotations

from typing import Any, Dict, List, Optional


class ComponentRegistry:
    def __init__(self) -> None:
        self._components: Dict[str, Any] = {}

    def register(self, name: str, component: Any) -> None:
        self._components[name] = component

    def unregister(self, name: str) -> None:
        self._components.pop(name, None)

    def get(self, name: str) -> Optional[Any]:
        return self._components.get(name)

    def require(self, name: str) -> Any:
        component = self.get(name)
        if component is None:
            raise KeyError(f"Component not registered: {name}")
        return component

    def exists(self, name: str) -> bool:
        return name in self._components

    def names(self) -> List[str]:
        return sorted(self._components.keys())

    def count(self) -> int:
        return len(self._components)

    def all(self) -> Dict[str, Any]:
        return self._components.copy()

    def clear(self) -> None:
        self._components.clear()


class ServiceRegistry(ComponentRegistry):
    def registry_type(self) -> str:
        return "service"


class ManagerRegistry(ComponentRegistry):
    def registry_type(self) -> str:
        return "manager"


class EngineRegistry(ComponentRegistry):
    def registry_type(self) -> str:
        return "engine"


class RepositoryRegistry(ComponentRegistry):
    def registry_type(self) -> str:
        return "repository"


service_registry = ServiceRegistry()
manager_registry = ManagerRegistry()
engine_registry = EngineRegistry()
repository_registry = RepositoryRegistry()
