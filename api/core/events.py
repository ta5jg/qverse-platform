

from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional


class Event:
    def __init__(
        self,
        name: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.name = name
        self.payload = payload or {}
        self.timestamp = datetime.now(timezone.utc)


class EventHandler:
    def __init__(self, callback: Callable[[Event], None]) -> None:
        self.callback = callback

    def handle(self, event: Event) -> None:
        self.callback(event)


class EventRegistry:
    def __init__(self) -> None:
        self._handlers: Dict[str, List[EventHandler]] = {}

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        self._handlers.setdefault(event_name, []).append(handler)

    def unsubscribe(self, event_name: str, handler: EventHandler) -> None:
        if event_name in self._handlers:
            self._handlers[event_name] = [
                h for h in self._handlers[event_name] if h is not handler
            ]

    def handlers(self, event_name: str) -> List[EventHandler]:
        return self._handlers.get(event_name, []).copy()


class EventBus:
    def __init__(self, registry: EventRegistry) -> None:
        self.registry = registry

    def publish(self, event: Event) -> int:
        handlers = self.registry.handlers(event.name)

        for handler in handlers:
            handler.handle(event)

        return len(handlers)


class EventMetrics:
    def __init__(self) -> None:
        self.events_published = 0
        self.handlers_executed = 0

    def record_publish(self, handlers_count: int) -> None:
        self.events_published += 1
        self.handlers_executed += handlers_count


registry = EventRegistry()
event_bus = EventBus(registry)
event_metrics = EventMetrics()