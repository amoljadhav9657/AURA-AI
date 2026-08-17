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
                    # Task Management
        elif (
            "what is my task status" in text
            or "task status" in text
            or text == "status"
        ):
            return "task_status"

        elif (
            "task progress" in text
            or "my task progress" in text
            or "progress of my task" in text
        ):
            return "task_progress"

        elif (
            text.startswith("start subtask ")
            or text.startswith("start task step ")
        ):
            return "subtask_start"

        elif (
            text.startswith("complete subtask ")
            or text.startswith("complete task step ")
        ):
            return "subtask_complete"

        elif (
            text.startswith("fail subtask ")
            or text.startswith("fail task step ")
        ):
            return "subtask_fail"

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

        # Task Management
        elif (
            "task progress" in text
            or "my task progress" in text
            or "progress of my task" in text
        ):
            return "task_progress"

        elif (
            text.startswith("start subtask ")
            or text.startswith("start task step ")
        ):
            return "subtask_start"

        elif (
            text.startswith("complete subtask ")
            or text.startswith("complete task step ")
        ):
            return "subtask_complete"

        elif (
            text.startswith("fail subtask ")
            or text.startswith("fail task step ")
        ):
            return "subtask_fail"

        # Task Status
        elif (
            "what is my task status" in text
            or "task status" in text
            or text == "status"
        ):
            return "task_status"

        # Complete Main Task
        elif (
            text == "complete the task"
            or text == "complete task"
            or text == "finish the task"
            or text == "finish task"
        ):
            return "task_complete"

        # Task Commands
        elif (
            text.startswith("create a task ")
            or text.startswith("create task ")
            or text.startswith("add a task ")
            or text.startswith("new task ")
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
