

from typing import Any, Callable, Dict, Optional


class Container:
    def __init__(self) -> None:
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, Callable[[], Any]] = {}

    def register_instance(self, name: str, instance: Any) -> None:
        self._services[name] = instance

    def register_factory(self, name: str, factory: Callable[[], Any]) -> None:
        self._factories[name] = factory

    def resolve(self, name: str) -> Optional[Any]:
        if name in self._services:
            return self._services[name]

        if name in self._factories:
            instance = self._factories[name]()
            self._services[name] = instance
            return instance

        return None

    def exists(self, name: str) -> bool:
        return name in self._services or name in self._factories

    def unregister(self, name: str) -> None:
        self._services.pop(name, None)
        self._factories.pop(name, None)

    def clear(self) -> None:
        self._services.clear()
        self._factories.clear()

    def services(self) -> Dict[str, Any]:
        return self._services.copy()

    def factories(self) -> Dict[str, Callable[[], Any]]:
        return self._factories.copy()


container = Container()