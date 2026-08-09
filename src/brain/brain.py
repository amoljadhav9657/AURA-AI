"""
=========================================
AURA AI - Brain
Version : 0.11.0
=========================================
"""

from .intent_classifier import IntentClassifier
from .decision_engine import DecisionEngine
from src.memory.memory_manager import MemoryManager
from src.system.system_manager import SystemManager


class Brain:

    def __init__(self):
        self.intent = IntentClassifier()
        self.engine = DecisionEngine()
        self.memory = MemoryManager()
        self.system = SystemManager()

    def process(self, text):

        text = text.strip()

        if not text:
            return "Please say something."

        # System commands first
        result = self.system.execute(text)

        if result:
            return result

        # Detect intent
        intent = self.intent.detect(text)

        # Save user's name
        if intent == "memory_save_name":

            name = text[11:].strip()

            if name:
                self.memory.remember("name", name)
                return f"Nice to meet you, {name}."

            return "Please tell me your name."

        # Recall user's name
        if intent == "memory_recall_name":

            name = self.memory.recall("name")

            if name:
                return f"Your name is {name}."

            return "I don't know your name yet."

        # Natural memory save
        if intent == "memory_save":

            statement = text[len("remember that "):].strip()

            if not statement:
                return "What would you like me to remember?"

            if " is " in statement:

                key, value = statement.split(" is ", 1)

                key = key.strip()
                value = value.strip()

                # Remove "my" prefix
                if key.startswith("my "):
                    key = key[3:].strip()

                if key and value:
                    self.memory.remember(key, value)
                    return f"I'll remember that your {key} is {value}."

            return "I can remember facts in the form: remember that X is Y."

        # Natural memory recall
        if intent == "memory_recall":

            key = text[len("what is my "):].strip().rstrip("?")

            if key:

                value = self.memory.recall(key)

                if value:
                    return f"Your {key} is {value}."

                return f"I don't know your {key} yet."

            return "What would you like me to recall?"

        # Normal AI processing
        return self.engine.execute(intent)