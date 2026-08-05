from .intent_classifier import IntentClassifier
from .decision_engine import DecisionEngine
from src.memory.memory import Memory


class Brain:

    def __init__(self):
        self.intent = IntentClassifier()
        self.engine = DecisionEngine()
        self.memory = Memory()

    def process(self, text):

        lower = text.lower().strip()

        # Save user's name
        if lower.startswith("my name is "):
            name = text[11:].strip()
            self.memory.remember("name", name)
            return f"Nice to meet you, {name}."

        # Recall user's name
        if "what is my name" in lower:
            name = self.memory.recall("name")

            if name:
                return f"Your name is {name}."

            return "I don't know your name yet."

        # Normal AI processing
        intent = self.intent.detect(text)
        return self.engine.execute(intent)