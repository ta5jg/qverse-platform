class VectorMemory:
    def __init__(self):
        self.records = list()

    def add(self, text, metadata=None):
        item = {"id": len(self.records) + 1, "text": text, "metadata": metadata or {}}
        self.records.append(item)
        return item

    def search(self, query, limit=5):
        hits = [item for item in self.records if query.lower() in item["text"].lower()]
        return hits[:limit]

vector_memory = VectorMemory()
