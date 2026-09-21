from src.system.desktop_engine import DesktopEngine


class Orchestrator:

    def __init__(self, brain):

        self.brain = brain

        # Desktop / application control
        self.desktop = DesktopEngine()

    def handle(self, text):

        if not text or not text.strip():

            return "Please say something."

        text = text.strip()

        intent = self.brain.intent.detect(text)

        # =====================================================
        # DESKTOP / APPLICATION ACTIONS
        # =====================================================

        if intent == "system_action":

            result = self.desktop.execute(text)

            if result:

                return result

            # If Desktop Engine does not understand
            # the command, let the existing Brain handle it.
            return self.brain.process(text)

        # =====================================================
        # TASK REQUESTS
        # =====================================================

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

        # =====================================================
        # MEMORY / CONTEXT
        # =====================================================

        if intent in {
            "memory_save",
            "memory_recall",
            "memory_save_name",
            "memory_recall_name",
            "memory_auto_save",
        }:

            return self.brain.process(text)

        # =====================================================
        # EVERYTHING ELSE
        # =====================================================

        return self.brain.process(text)
