from src.task.task_planner import TaskPlanner
from src.executor.task_executor import TaskExecutor


class TaskManager:

    def __init__(self):
        self.planner = TaskPlanner()
        self.executor = TaskExecutor()

    def create_and_start(self, task):
        if not task or not task.strip():
            return {
                "status": "error",
                "message": "Task cannot be empty."
            }

        planned = self.planner.create_task(task)

        if not planned:
            return {
                "status": "error",
                "message": "Task could not be created."
            }

        execution = self.executor.start(planned["task"])

        return {
            "status": execution["status"],
            "task": planned["task"],
            "planned": planned,
            "execution": execution
        }

    def complete_current(self):
        return self.executor.complete()

    def fail_current(self, reason):
        return self.executor.fail(reason)

    def get_status(self):
        return {
            "planner": self.planner.get_tasks(),
            "executor": self.executor.get_status()
        }

    def reset(self):
        self.planner.clear_tasks()
        self.executor.reset()
