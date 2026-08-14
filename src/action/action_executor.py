from src.system.system_manager import SystemManager


class ActionExecutor:

    def __init__(self):
        self.system = SystemManager()
        self.last_action = None
        self.status = "idle"

    def execute(self, action, target=None):

        if not action:
            return {
                "status": "error",
                "message": "No action provided."
            }

        action = action.strip()

        self.last_action = {
            "action": action,
            "target": target
        }

        # Open application
        if action == "open_app":

            if not target:
                self.status = "error"

                return {
                    "status": "error",
                    "message": "No application provided."
                }

            result = self.system.execute(
                f"open {target}"
            )

            if result:

                self.status = "completed"

                return {
                    "status": "completed",
                    "action": action,
                    "target": target,
                    "result": result
                }

            self.status = "failed"

            return {
                "status": "failed",
                "action": action,
                "target": target
            }

        # Open browser website
        if action == "open_browser":

            if not target:
                self.status = "error"

                return {
                    "status": "error",
                    "message": "No website provided."
                }

            result = self.system.execute(
                f"open {target}"
            )

            if result:

                self.status = "completed"

                return {
                    "status": "completed",
                    "action": action,
                    "target": target,
                    "result": result
                }

            self.status = "failed"

            return {
                "status": "failed",
                "action": action,
                "target": target
            }

        self.status = "ready"

        return {
            "status": "ready",
            "action": action,
            "target": target
        }

    def get_status(self):

        return {
            "status": self.status,
            "last_action": self.last_action
        }

    def reset(self):

        self.last_action = None
        self.status = "idle"
