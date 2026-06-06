class EventBus:
    def __init__(self):
        self.events = []

    def publish(self, topic, payload=None):
        event = {"id": len(self.events) + 1, "topic": topic, "payload": payload or {}}
        self.events.append(event)
        return event

    def list_events(self):
        return self.events

event_bus = EventBus()\n