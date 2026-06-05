class MemoryManager:
    def __init__(self):
        self._records = {}

    def save(self, key, value):
        self._records[key] = value
        return {"status": "ok", "saved_key": key}

    def get(self, key):
        if key in self._records:
            return {"status": "ok", "key": key, "value": self._records[key]}
        return {"status": "not_found", "key": key}

    def list_items(self):
        return {"status": "ok", "items": list(self._records.items())}

    def health(self):
        return {
            "status": "healthy",
            "item_count": len(self._records)
        }
