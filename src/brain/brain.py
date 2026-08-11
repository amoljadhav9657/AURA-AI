from .intent_classifier import IntentClassifier
from .decision_engine import DecisionEngine
from src.memory.memory_manager import MemoryManager
from src.system.system_manager import SystemManager
from src.context.context_engine import ContextEngine


class Brain:

    def __init__(self):
        self.intent = IntentClassifier()
        self.engine = DecisionEngine()
        self.memory = MemoryManager()
        self.system = SystemManager()
        self.context = ContextEngine(self.memory)

    def process(self, text):

        text = text.strip()

        if not text:
            return "Please say something."

        self.memory.remember_conversation("user", text)

        # System commands
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

        # Automatic Fact Memory
        if intent == "memory_auto_save":

            statement = text.strip()

            if statement.startswith("my "):
                statement = statement[3:].strip()

            if " is " in statement:

                key, value = statement.split(" is ", 1)

                key = key.strip()
                value = value.strip()

                if key and value:

                    self.memory.remember(key, value)

                    response = f"I'll remember that your {key} is {value}."
                    self.memory.remember_conversation("aura", response)
                    return response

            response = "I couldn't understand that fact."
            self.memory.remember_conversation("aura", response)
            return response

        # Context-aware processing
        if intent == "unknown":

            current_topic = self.context.get_current_topic()
            current_value = self.context.get_current_topic_value()
            is_follow_up = self.context.is_follow_up(text)

            # Resolve references such as it, this, that
            resolved = self.context.resolve_reference(text)

            if resolved:

                lower_text = text.lower()

                if "like it" in lower_text:
                    response = f"That's great! You really like {resolved}."

                elif "like this" in lower_text:
                    response = f"That's great! You really like {resolved}."

                elif "like that" in lower_text:
                    response = f"That's great! You really like {resolved}."

                elif "good" in lower_text:
                    response = f"Yes, {resolved} sounds good."

                else:
                    response = f"You are referring to {resolved}."

                self.memory.remember_conversation("aura", response)
                return response

            # Topic-aware response
            if current_topic and current_value and is_follow_up:

                lower_text = text.lower()

                if "tell me more" in lower_text:
                    response = (
                        f"Your current topic is your "
                        f"{current_topic}, and you mentioned {current_value}."
                    )

                elif "like" in lower_text:
                    response = (
                        f"That's great! You like your "
                        f"{current_topic}, {current_value}."
                    )

                elif "good" in lower_text:
                    response = f"Yes, {current_value} sounds good."

                elif "why" in lower_text:
                    response = (
                        f"We were talking about your "
                        f"{current_topic}, which is {current_value}."
                    )

                else:
                    response = (
                        f"We are still talking about your "
                        f"{current_topic}, {current_value}."
                    )

                self.memory.remember_conversation("aura", response)
                return response

            # Search previous context
            relevant_context = self.context.find_relevant_context(text)

            if relevant_context:

                last_context = relevant_context[-1]

                response = (
                    f"I remember you mentioned: "
                    f"{last_context['text']}"
                )

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
