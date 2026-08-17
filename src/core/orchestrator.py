class Orchestrator:

    def __init__(self, brain):
        self.brain = brain

    def handle(self, text):
        if not text or not text.strip():
            return "Please say something."

        text = text.strip()

        intent = self.brain.intent.detect(text)

        # Task requests
        if intent in {
            "task",
            "task_status",
            "task_progress",
            "task_complete",
            "subtask_start",
            "subtask_complete",
            "subtask_fail",
        }:
            return self.brain.process(text)

        # System / application actions
        if intent == "system_action":
            return self.brain.process(text)

        # Memory and context
        if intent in {
            "memory_save",
            "memory_recall",
            "memory_save_name",
            "memory_recall_name",
            "memory_auto_save",
        }:
            return self.brain.process(text)

        # Everything else
        return self.brain.process(text)
