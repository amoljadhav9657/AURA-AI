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

        # Save user message to short-term memory
        self.memory.remember_conversation("user", text)

        # System commands first
        result = self.system.execute(text)

        if result:
            self.memory.remember_conversation("aura", result)
            return result

        # Detect intent
        intent = self.intent.detect(text)

        # Save user's name
        if intent == "memory_save_name":

            name = text[11:].strip()

            if name:
                self.memory.remember("name", name)

                response = f"Nice to meet you, {name}."
                self.memory.remember_conversation("aura", response)
                return response

            response = "Please tell me your name."
            self.memory.remember_conversation("aura", response)
            return response

        # Recall user's name
        if intent == "memory_recall_name":

            name = self.memory.recall("name")

            if name:
                response = f"Your name is {name}."
            else:
                response = "I don't know your name yet."

            self.memory.remember_conversation("aura", response)
            return response

        # Natural memory save
        if intent == "memory_save":

            statement = text[len("remember that "):].strip()

            if not statement:
                response = "What would you like me to remember?"
                self.memory.remember_conversation("aura", response)
                return response

            if " is " in statement:

                key, value = statement.split(" is ", 1)

                key = key.strip()
                value = value.strip()

                if key.startswith("my "):
                    key = key[3:].strip()

                if key and value:

                    self.memory.remember(key, value)

                    response = f"I'll remember that your {key} is {value}."
                    self.memory.remember_conversation("aura", response)
                    return response

            response = "I can remember facts in the form: remember that X is Y."
            self.memory.remember_conversation("aura", response)
            return response

        # Natural memory recall
        if intent == "memory_recall":

            key = text[len("what is my "):].strip().rstrip("?")

            if key:

                value = self.memory.recall(key)

                if value:
                    response = f"Your {key} is {value}."
                else:
                    response = f"I don't know your {key} yet."

                self.memory.remember_conversation("aura", response)
                return response

            response = "What would you like me to recall?"
            self.memory.remember_conversation("aura", response)
            return response

        # Normal AI processing
        response = self.engine.execute(intent)

        self.memory.remember_conversation("aura", response)

        return response

    def get_recent_conversation(self):
        return self.memory.get_conversation()

    def clear_recent_conversation(self):
        self.memory.clear_conversation()