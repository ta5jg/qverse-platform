class AIMemory:
    def __init__(self):
        self._storage = {}

    def save(self, key, value):
        self._storage[key] = value
        return {"status": "ok", "saved_key": key}

    def get(self, key):
        if key in self._storage:
            return {"status": "ok", "key": key, "value": self._storage[key]}
        return {"status": "not_found", "key": key}

    def list_items(self):
        return {"status": "ok", "items": list(self._storage.items())}

    def health(self):
        return {
            "status": "healthy",
            "item_count": len(self._storage)
        }
