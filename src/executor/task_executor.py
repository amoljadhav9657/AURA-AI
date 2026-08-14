class TaskExecutor:

    def __init__(self):
        self.current_task = None
        self.status = "idle"

    def start(self, task):
        if not task:
            return {
                "status": "error",
                "message": "No task provided."
            }

        task = task.strip()

        if not task:
            return {
                "status": "error",
                "message": "Task cannot be empty."
            }

        self.current_task = task
        self.status = "running"

        return {
            "status": "running",
            "task": task
        }

    def complete(self):
        if not self.current_task:
            return {
                "status": "error",
                "message": "No active task."
            }

        task = self.current_task

        self.status = "completed"

        return {
            "status": "completed",
            "task": task
        }

    def fail(self, reason):
        if not self.current_task:
            return {
                "status": "error",
                "message": "No active task."
            }

        task = self.current_task

        self.status = "failed"

        return {
            "status": "failed",
            "task": task,
            "reason": reason
        }

    def get_status(self):
        return {
            "status": self.status,
            "task": self.current_task
        }

    def reset(self):
        self.current_task = None
        self.status = "idle"
