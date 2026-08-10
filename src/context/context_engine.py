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

            if word in ["it", "this", "that", "these", "those", "he", "she", "they"]:
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
