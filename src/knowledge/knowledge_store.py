class KnowledgeStore:

    def __init__(self):
        self.knowledge = []

    def add(self, fact, source="user", confidence=1.0):
        if not fact or not fact.strip():
            return None

        item = {
            "fact": fact.strip(),
            "source": source,
            "confidence": float(confidence)
        }

        self.knowledge.append(item)
        return item

    def get_all(self):
        return self.knowledge.copy()

    def search(self, query):
        if not query or not query.strip():
            return []

        query = query.lower().strip()

        return [
            item for item in self.knowledge
            if query in item["fact"].lower()
        ]

    def clear(self):
        self.knowledge.clear()
