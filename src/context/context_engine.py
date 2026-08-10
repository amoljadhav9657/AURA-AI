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

    def find_relevant_context(self, text):

        conversations = self.memory.get_conversation()

        if not conversations:
            return []

        words = text.lower().strip().split()

        relevant = []

        for message in conversations:

            # Only search previous user messages
            if message["role"] != "user":
                continue

            message_text = message["text"].lower()

            for word in words:

                if len(word) > 3 and word in message_text:
                    relevant.append(message)
                    break

        return relevant

    def last_aura_message(self):

        conversations = self.memory.get_conversation()

        for message in reversed(conversations):

            if message["role"] == "aura":
                return message["text"]

        return None
