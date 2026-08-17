cat > src/brain/reasoning.py <<'PY'
class ReasoningEngine:

    def __init__(self, knowledge_engine):
        self.knowledge = knowledge_engine

    def analyze(self, query):
        if not query or not query.strip():
            return {
                "status": "error",
                "message": "Query cannot be empty."
            }

        query = query.strip()
        results = self.knowledge.recall(query)

        if not results:
            return {
                "status": "unknown",
                "query": query,
                "facts": [],
                "best": None,
                "conclusion": None
            }

        best = self.knowledge.recall_best(query)
        conclusion = self._infer(results)

        return {
            "status": "known",
            "query": query,
            "facts": results,
            "best": best,
            "conclusion": conclusion
        }

    def _infer(self, facts):
        if not facts:
            return None

        if len(facts) == 1:
            return facts[0]["fact"]

        high_confidence = [
            fact
            for fact in facts
            if fact.get("confidence", 0.0) >= 0.8
        ]

        if len(high_confidence) == 1:
            return high_confidence[0]["fact"]

        if len(high_confidence) > 1:
            return (
                "Multiple high-confidence facts support "
                "this information."
            )

        return (
            "Multiple facts are available, but their "
            "confidence is limited."
        )
PY