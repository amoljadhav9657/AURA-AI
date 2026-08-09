"""
=========================================
AURA AI - Brain
Version : 0.10.0
=========================================
"""

from .intent_classifier import IntentClassifier
from .decision_engine import DecisionEngine
from src.memory.memory import Memory
from src.system.system_manager import SystemManager


class Brain:

    def __init__(self):
        self.intent = IntentClassifier()
        self.engine = DecisionEngine()
        self.memory = Memory()
        self.system = SystemManager()

    def process(self, text):

        text = text.strip()

        if not text:
            return "Please say something."

        # Check system commands first
        result = self.system.execute(text)

        if result:
            return result

        # Detect intent
        intent = self.intent.detect(text)

        # Memory - Save
        if intent == "memory_save":

            name = text[11:].strip()

            if name:
                self.memory.remember("name", name)
                return f"Nice to meet you, {name}."

            return "Please tell me your name."

        # Memory - Recall
        if intent == "memory_recall":

            name = self.memory.recall("name")

            if name:
                return f"Your name is {name}."

            return "I don't know your name yet."

        # Normal AI processing
        return self.engine.execute(intent)