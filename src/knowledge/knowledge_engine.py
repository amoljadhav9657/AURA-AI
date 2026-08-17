from src.knowledge.knowledge_store import KnowledgeStore


class KnowledgeEngine:

    def __init__(self):
        self.store = KnowledgeStore()

    def learn(self, fact, source="user", confidence=1.0):
        return self.store.add(
            fact,
            source=source,
            confidence=confidence
        )

    def recall(self, query):
        return self.store.search(query)

    def get_all(self):
        return self.store.get_all()

    def clear(self):
        self.store.clear()

    def recall_best(self, query):
        results = self.recall(query)

        if not results:
            return None

        return max(
            results,
            key=lambda item: item.get("confidence", 0.0)
        )
