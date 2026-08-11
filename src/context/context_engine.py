class ContextEngine:

    def __init__(self, memory):
        self.memory = memory

    def get_recent_context(self, limit=5):
        conversations = self.memory.get_conversation()

        if not conversations:
            return []

        return conversations[-limit:]

    def last_user_message(self):
        conversations = self.memory.get_conversation()

        for message in reversed(conversations):
            if message["role"] == "user":
                return message["text"]

        return None

    def last_aura_message(self):
        conversations = self.memory.get_conversation()

        for message in reversed(conversations):
            if message["role"] == "aura":
                return message["text"]

        return None

    def find_relevant_context(self, text):
        conversations = self.memory.get_conversation()

        if not conversations:
            return []

        words = text.lower().strip().split()
        relevant = []

        for message in conversations:
            if message["role"] != "user":
                continue

            message_text = message["text"].lower()

            for word in words:
                word = word.strip(".,!?")

                if len(word) > 3 and word in message_text:
                    relevant.append(message)
                    break

        return relevant

    def find_reference(self, text):
        words = text.lower().strip().split()

        references = []

        for word in words:
            word = word.strip(".,!?")

            if word in [
                "it",
                "this",
                "that",
                "these",
                "those",
                "he",
                "she",
                "they"
            ]:
                references.append(word)

        return references

    def resolve_reference(self, text):
        references = self.find_reference(text)

        if not references:
            return None

        conversations = self.memory.get_conversation()

        if not conversations:
            return None

        for message in reversed(conversations[:-1]):

            if message["role"] != "user":
                continue

            previous_text = message["text"]

            if " is " in previous_text:

                key, value = previous_text.split(" is ", 1)

                key = key.strip()
                value = value.strip().rstrip(".,!?")

                if key.startswith("my "):
                    key = key[3:].strip()

                if value:
                    return value

        return None

    # v0.16.0 - Topic Tracking

    def detect_topic(self):
        conversations = self.memory.get_conversation()

        if not conversations:
            return None

        for message in reversed(conversations):

            if message["role"] != "user":
                continue

            text = message["text"].lower().strip()

            if text.startswith("my ") and " is " in text:

                statement = text[3:].strip()

                key, value = statement.split(" is ", 1)

                key = key.strip()
                value = value.strip().rstrip(".,!?")

                if key and value:
                    return {
                        "key": key,
                        "value": value
                    }

        return None

    def get_current_topic(self):
        topic = self.detect_topic()

        if not topic:
            return None

        return topic["key"]

    def get_current_topic_value(self):
        topic = self.detect_topic()

        if not topic:
            return None

        return topic["value"]
            # v0.17.0 - Conversation State

    def get_current_state(self):
        topic = self.detect_topic()

        if not topic:
            return {
                "topic": None,
                "value": None
            }

        return {
            "topic": topic["key"],
            "value": topic["value"]
        }

    def is_follow_up(self, text):
        text = text.lower().strip()

        references = self.find_reference(text)

        if references:
            return True

        follow_up_phrases = [
            "what about",
            "how about",
            "and",
            "also",
            "but",
            "then",
            "why",
            "how",
            "really",
            "tell me more"
        ]

        for phrase in follow_up_phrases:
            if text.startswith(phrase + " ") or text == phrase:
                return True

        return False

    def get_context_summary(self):
        state = self.get_current_state()

        if not state["topic"]:
            return "No active topic."

        return f"Current topic: {state['topic']}. Current value: {state['value']}."
