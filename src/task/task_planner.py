class TaskPlanner:

    def __init__(self):
        self.tasks = []

    def create_task(self, task):
        if not task:
            return None

        task = task.strip()

        if not task:
            return None

        self.tasks.append(task)

        return {
            "task": task,
            "status": "created"
        }

    def get_tasks(self):
        return self.tasks.copy()

    def clear_tasks(self):
        self.tasks.clear()

    def has_tasks(self):
        return len(self.tasks) > 0
