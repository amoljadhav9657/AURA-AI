class ContextEngine:

    def __init__(self, memory):
        self.memory = memory
        self.active_topic = None

    # ---------------------------------------------------------
    # Conversation
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # Relevant Context
    # ---------------------------------------------------------

    def find_relevant_context(self, text):
        conversations = self.memory.get_conversation()

        if not conversations:
            return []

        words = text.lower().strip().split()
        relevant = []

        # The current user message is already stored in memory
        # before context search. Do not match the message against
        # itself; only search previous user messages.
        user_messages = [
            message
            for message in conversations
            if message["role"] == "user"
        ]

        previous_messages = user_messages[:-1]

        for message in previous_messages:

            message_text = message["text"].lower()

            # Do not treat a repeated standalone/unknown query
            # as meaningful conversation context.
            if message_text.strip() == text.lower().strip():
                continue

            meaningful_words = [
                word.strip(".,!?")
                for word in words
                if len(word.strip(".,!?")) > 3
            ]

            # Require at least one meaningful overlap, but ignore
            # generic/weak conversational words.
            ignored_words = {
                "hello",
                "what",
                "know",
                "about",
                "tell",
                "this",
                "that",
                "really",
                "good",
                "help",
                "please",
            }

            meaningful_words = [
                word
                for word in meaningful_words
                if word not in ignored_words
            ]

            if not meaningful_words:
                continue

            matches = [
                word
                for word in meaningful_words
                if word in message_text
            ]

            if matches:
                relevant.append(message)

        return relevant

    # ---------------------------------------------------------
    # References
    # ---------------------------------------------------------

    def find_reference(self, text):
        words = text.lower().strip().split()

        references = []

        reference_words = {
            "it",
            "this",
            "that",
            "these",
            "those",
            "he",
            "she",
            "they",
        }

        for word in words:
            word = word.strip(".,!?")

            if word in reference_words:
                references.append(word)

        return references

    def resolve_reference(self, text):
        references = self.find_reference(text)

        if not references:
            return None

        if not self.active_topic:
            return None

        return self.active_topic["value"]

    # ---------------------------------------------------------
    # Topic Extraction
    # ---------------------------------------------------------

    def _extract_topic(self, text):
        text = text.lower().strip()

        if not text.startswith("my "):
            return None

        if " is " not in text:
            return None

        statement = text[3:].strip()

        key, value = statement.split(" is ", 1)

        key = key.strip()
        value = value.strip().rstrip(".,!?")

        if not key or not value:
            return None

        return {
            "key": key,
            "value": value,
        }

    def get_all_topics(self):
        memories = self.memory.get_all_memories()

        topics = []

        for memory in memories:
            key = memory.get("key")
            value = memory.get("value")

            if not key or not value:
                continue

            key = key.strip()
            value = value.strip()

            # Ignore old/test/non-topic memories.
            if key in {
                "name",
                "test_key",
                "favorite_food",
                "favorite_color",
            }:
                continue

            # Only favorite-* facts are topics for this version.
            if key.startswith("favorite "):
                topics.append({
                    "key": key,
                    "value": value,
                })

        return topics

    def detect_topic(self):
        topics = self.get_all_topics()

        if not topics:
            return None

        return topics[-1]

    # ---------------------------------------------------------
    # Explicit Topic Matching
    # ---------------------------------------------------------

    def find_topic(self, text):
        text = text.lower().strip().rstrip("?!. ")

        if not text:
            return None

        topics = self.get_all_topics()

        if not topics:
            return None

        # 1. Exact/full topic key.
        for topic in reversed(topics):
            key = topic["key"].lower().strip()

            if key and key in text:
                return topic

        # 2. Meaningful topic words.
        for topic in reversed(topics):
            key = topic["key"].lower().strip()

            words = [
                word
                for word in key.split()
                if len(word) > 2 and word != "favorite"
            ]

            if words and all(word in text for word in words):
                return topic

        # 3. Short topic references:
        #    color / food / sport
        for topic in reversed(topics):
            key = topic["key"].lower().strip()

            words = [
                word
                for word in key.split()
                if len(word) > 2 and word != "favorite"
            ]

            for word in words:
                if word in text:
                    return topic

        return None

    # ---------------------------------------------------------
    # Topic State
    # ---------------------------------------------------------

    def set_active_topic(self, topic):
        if not topic:
            return None

        self.active_topic = {
            "key": topic["key"],
            "value": topic["value"],
        }

        return self.active_topic

    def switch_topic(self, text):
        topic = self.find_topic(text)

        if not topic:
            return None

        return self.set_active_topic(topic)

    def get_active_topic(self):
        return self.active_topic

    def clear_active_topic(self):
        self.active_topic = None

    def get_current_topic(self):
        if not self.active_topic:
            return None

        return self.active_topic["key"]

    def get_current_topic_value(self):
        if not self.active_topic:
            return None

        return self.active_topic["value"]

    # ---------------------------------------------------------
    # Follow-up
    # ---------------------------------------------------------

    def is_follow_up(self, text):
        text = text.lower().strip()

        if self.find_reference(text):
            return True

        phrases = [
            "what about",
            "how about",
            "and",
            "also",
            "but",
            "then",
            "why",
            "how",
            "really",
            "tell me more",
        ]

        for phrase in phrases:
            if text == phrase:
                return True

            if text.startswith(phrase + " "):
                return True

        return False

    # ---------------------------------------------------------
    # State
    # ---------------------------------------------------------

    def get_current_state(self):
        if not self.active_topic:
            return {
                "topic": None,
                "value": None,
            }

        return {
            "topic": self.active_topic["key"],
            "value": self.active_topic["value"],
        }

    def get_previous_topic(self):
        topics = self.get_all_topics()

        if len(topics) < 2:
            return None

        if not self.active_topic:
            return topics[-2]

        for topic in reversed(topics):
            if topic != self.active_topic:
                return topic

        return None

    def get_context_state(self):
        return {
            "active_topic": self.active_topic,
            "previous_topic": self.get_previous_topic(),
            "history": self.get_all_topics(),
        }

    def get_context_summary(self):
        state = self.get_current_state()

        if not state["topic"]:
            return "No active topic."

        return (
            f"Current topic: {state['topic']}. "
            f"Current value: {state['value']}."
        )

    def get_topic_history(self):
        return self.get_all_topics()
