class TaskDecomposer:

    def __init__(self):
        self.subtasks = []

    def decompose(self, task):
        if not task:
            return []

        task = task.strip()

        if not task:
            return []

        lower_task = task.lower()

        if "website" in lower_task:
            steps = [
                "Understand requirements",
                "Create project structure",
                "Build frontend",
                "Build backend",
                "Add database",
                "Test application",
                "Fix errors",
                "Report completion"
            ]

        elif "video game" in lower_task or "game" in lower_task:
            steps = [
                "Understand game requirements",
                "Create game project structure",
                "Implement game logic",
                "Add user interface",
                "Add assets",
                "Test the game",
                "Fix errors",
                "Report completion"
            ]

        else:
            steps = [
                f"Understand requirements for: {task}",
                "Plan the required steps",
                "Execute the planned steps",
                "Test the result",
                "Report completion"
            ]

        self.subtasks = [
            {
                "id": index,
                "task": step,
                "status": "pending"
            }
            for index, step in enumerate(steps, start=1)
        ]

        return self.subtasks.copy()

    def start_subtask(self, subtask_id):
        subtask = self._find_subtask(subtask_id)

        if not subtask:
            return {
                "status": "error",
                "message": "Subtask not found."
            }

        if subtask["status"] == "completed":
            return {
                "status": "error",
                "message": "Subtask is already completed."
            }

        subtask["status"] = "running"

        return subtask.copy()

    def complete_subtask(self, subtask_id):
        subtask = self._find_subtask(subtask_id)

        if not subtask:
            return {
                "status": "error",
                "message": "Subtask not found."
            }

        subtask["status"] = "completed"

        return subtask.copy()

    def fail_subtask(self, subtask_id, reason=""):
        subtask = self._find_subtask(subtask_id)

        if not subtask:
            return {
                "status": "error",
                "message": "Subtask not found."
            }

        subtask["status"] = "failed"
        subtask["reason"] = reason

        return subtask.copy()

    def get_subtask(self, subtask_id):
        subtask = self._find_subtask(subtask_id)

        if not subtask:
            return None

        return subtask.copy()

    def get_subtasks(self):
        return [subtask.copy() for subtask in self.subtasks]

    def get_progress(self):
        total = len(self.subtasks)

        if total == 0:
            return {
                "total": 0,
                "completed": 0,
                "progress": 0.0
            }

        completed = sum(
            1
            for subtask in self.subtasks
            if subtask["status"] == "completed"
        )

        progress = (completed / total) * 100

        return {
            "total": total,
            "completed": completed,
            "progress": progress
        }

    def clear(self):
        self.subtasks.clear()

    def has_subtasks(self):
        return len(self.subtasks) > 0

    def _find_subtask(self, subtask_id):
        for subtask in self.subtasks:
            if subtask["id"] == subtask_id:
                return subtask

        return None
