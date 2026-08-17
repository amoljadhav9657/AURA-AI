class ReasoningEngine:

    def __init__(self, knowledge_engine):
        self.knowledge = knowledge_engine

    def analyze(self, query):
        if not query or not query.strip():
            return {
                "status": "error",
                "message": "Query cannot be empty."
            }

        results = self.knowledge.recall(query)

        if not results:
            return {
                "status": "unknown",
                "query": query.strip(),
                "facts": [],
                "best": None
            }

        best = self.knowledge.recall_best(query)

        return {
            "status": "known",
            "query": query.strip(),
            "facts": results,
            "best": best
        }
