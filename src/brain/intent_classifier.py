"""
=========================================
AURA AI - Intent Classifier
Version : 0.10.0
=========================================
"""


class IntentClassifier:

    def detect(self, text: str) -> str:

        text = text.lower().strip()

        # Greeting
        if any(word in text for word in ["hello", "hi", "hey"]):
            return "greeting"

        # Time
        elif "time" in text:
            return "time"

        # Date
        elif "date" in text:
            return "date"

        # Memory
        elif text.startswith("my name is "):
            return "memory_save"

        elif "what is my name" in text:
            return "memory_recall"

        # Unknown
        else:
            return "unknown"