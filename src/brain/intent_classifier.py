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

        # Memory - Name
        elif text.startswith("my name is "):
            return "memory_save_name"

        elif "what is my name" in text:
            return "memory_recall_name"

        # Natural Memory
        elif text.startswith("remember that "):
            return "memory_save"

        elif text.startswith("what is my "):
            return "memory_recall"

        # Automatic Fact Detection
        elif text.startswith("my ") and " is " in text:
            return "memory_auto_save"

        # System / Action Commands
        elif (
            text.startswith("open ")
            or text.startswith("launch ")
            or text.startswith("go to ")
            or text.startswith("search ")
            or text.startswith("search for ")
            or text.startswith("find ")
            or text.startswith("look up ")
        ):
            return "system_action"

        # Unknown
        else:
            return "unknown"