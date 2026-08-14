class ActionExecutor:

    def __init__(self):
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
