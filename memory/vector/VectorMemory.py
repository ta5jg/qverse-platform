class VectorMemory:
    def __init__(self):
        self.items = []

    def add(self, text, metadata=None):
        item = {"id": len(self.items) + 1, "text": text, "metadata": metadata or {}}
        self.items.append(item)
        return item

    def search(self, query, limit=5):
        hits = [item for item in self.items if query.lower() in item["text"].lower()]
        return hits[:limit]

vector_memory = VectorMemory()\n