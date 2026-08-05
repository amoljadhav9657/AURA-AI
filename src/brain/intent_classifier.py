"""
=========================================
AURA AI - Intent Classifier
Version : 0.1.0
=========================================
"""


class IntentClassifier:

    def detect(self, text: str) -> str:

        text = text.lower().strip()

        if any(word in text for word in ["hello", "hi", "hey"]):
            return "greeting"

        elif "time" in text:
            return "time"

        elif "date" in text:
            return "date"

        else:
            return "unknown"