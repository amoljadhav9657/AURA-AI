class TaskAnalyzerV2:

    def analyze(self, task):

        if not isinstance(task, str) or not task.strip():
            raise ValueError("Development task is required.")

        text = task.strip().lower()

        if any(x in text for x in [
            "website",
            "web app",
            "web application"
        ]):
            task_type = "website"

        elif any(x in text for x in [
            "excel",
            "xlsx",
            "spreadsheet"
        ]):
            task_type = "excel"

        elif any(x in text for x in [
            "database",
            "sqlite",
            "mysql",
            "postgres"
        ]):
            task_type = "database"

        elif any(x in text for x in [
            "software",
            "application",
            "desktop app",
            "python app"
        ]):
            task_type = "software"

        else:
            task_type = "general"

        return {
            "task": task.strip(),
            "task_type": task_type,
            "complexity": self._complexity(text)
        }

    def _complexity(self, text):

        words = len(text.split())

        if words > 80:
            return "high"

        if words > 30:
            return "medium"

        return "low"
