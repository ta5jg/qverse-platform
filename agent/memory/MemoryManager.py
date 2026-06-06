class MemoryManager:
    def __init__(self):
        self._records = {}

    def save(self, key, value):
        self._records[key] = value
        return {"status": "ok", "saved_key": key}

    def save_memory(self, key: str, value):
        return self.save(key, value)

    def get(self, key):
        if key in self._records:
            return {"status": "ok", "key": key, "value": self._records[key]}
        return {"status": "not_found", "key": key}

    def recall(self, key: str):
        result = self.get(key)
        if result.get("status") == "ok":
            return [{"key": key, "value": result.get("value")}]
        return []

    def list_items(self):
        return {"status": "ok", "items": list(self._records.items())}

    def list_memories(self):
        result = self.list_items()
        return [{"key": key, "value": value} for key, value in result.get("items", [])]

    def health(self):
        return {
            "status": "healthy",
            "item_count": len(self._records),
        }
