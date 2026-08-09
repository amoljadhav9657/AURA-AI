"""
=========================================
AURA AI - Intent Classifier
Version : 0.11.0
=========================================
"""


class IntentClassifier:

    def detect(self, text: str) -> str:

        text = text.lower().strip()

        # Greeting
        if any(word in text.split() for word in ["hello", "hi", "hey"]):
            return "greeting"

        # Time
        elif "time" in text:
            return "time"

        # Date
        elif "date" in text:
            return "date"

        # Natural Memory Save
        elif text.startswith("remember that "):
            return "memory_save"

        # Name Memory Save
        elif text.startswith("my name is "):
            return "memory_save_name"

        # Natural Memory Recall
        elif text.startswith("what is my "):
            return "memory_recall"

        # Name Memory Recall
        elif "what is my name" in text:
            return "memory_recall_name"

        # Unknown
        else:
            return "unknown"