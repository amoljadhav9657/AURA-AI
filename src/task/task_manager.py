from src.task.task_planner import TaskPlanner
from src.task.task_decomposer import TaskDecomposer
from src.executor.task_executor import TaskExecutor


class TaskManager:

    def __init__(self):
        self.planner = TaskPlanner()
        self.decomposer = TaskDecomposer()
        self.executor = TaskExecutor()

    def normalize_task(self, task):
        task = task.strip()

        prefixes = [
            "create a task ",
            "create task ",
            "add a task ",
            "new task "
        ]

        lower_task = task.lower()

        for prefix in prefixes:
            if lower_task.startswith(prefix):
                return task[len(prefix):].strip()

        return task

    def create_and_start(self, task):
        if not task or not task.strip():
            return {
                "status": "error",
                "message": "Task cannot be empty."
            }

        task = self.normalize_task(task)

        if not task:
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

        subtasks = self.decomposer.decompose(task)

        execution = self.executor.start(planned["task"])

        return {
            "status": execution["status"],
            "task": planned["task"],
            "planned": planned,
            "subtasks": subtasks,
            "execution": execution
        }

    def start_subtask(self, subtask_id):
        return self.decomposer.start_subtask(subtask_id)

    def complete_subtask(self, subtask_id):
        return self.decomposer.complete_subtask(subtask_id)

    def fail_subtask(self, subtask_id, reason=""):
        return self.decomposer.fail_subtask(
            subtask_id,
            reason
        )

    def get_subtask(self, subtask_id):
        return self.decomposer.get_subtask(subtask_id)

    def get_progress(self):
        return self.decomposer.get_progress()

    def complete_current(self):
        return self.executor.complete()

    def fail_current(self, reason):
        return self.executor.fail(reason)

    def get_status(self):
        return {
            "planner": self.planner.get_tasks(),
            "subtasks": self.decomposer.get_subtasks(),
            "progress": self.decomposer.get_progress(),
            "executor": self.executor.get_status()
        }

    def reset(self):
        self.planner.clear_tasks()
        self.decomposer.clear()
        self.executor.reset()
