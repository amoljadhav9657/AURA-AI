class IntentClassifier:

    def detect(self, text: str) -> str:

        text = text.lower().strip()

        # Greeting
        if text in ["hello", "hi", "hey"]:
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

        # Task Management Commands
        elif (
            "what is my task status" in text
            or "task status" in text
            or text == "status"
        ):
            return "task_status"

        elif (
            text == "complete the task"
            or text == "complete task"
            or text == "finish the task"
            or text == "finish task"
        ):
            return "task_complete"

        # Natural Memory Recall
        elif text.startswith("what is my "):
            return "memory_recall"

        # Automatic Fact Detection
        elif text.startswith("my ") and " is " in text:
            return "memory_auto_save"

        # Task Commands
        elif (
            text.startswith("create a task ")
            or text.startswith("plan ")
            or text.startswith("build ")
            or text.startswith("make ")
            or text.startswith("do ")
        ):
            return "task"

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
