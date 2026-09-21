class TaskAnalyzer:

    SOFTWARE_KEYWORDS = [
        "software",
        "application",
        "app",
        "program",
        "desktop app",
        "python app",
        "billing software",
        "inventory software"
    ]

    WEBSITE_KEYWORDS = [
        "website",
        "web site",
        "web application",
        "web app",
        "flask website",
        "dashboard"
    ]

    DATABASE_KEYWORDS = [
        "database",
        "sqlite",
        "mysql",
        "postgresql",
        "database system"
    ]

    EXCEL_KEYWORDS = [
        "excel",
        "spreadsheet",
        "xlsx",
        "xls"
    ]

    def analyze(self, task):

        if not isinstance(task, str) or not task.strip():
            raise ValueError("Development task is required.")

        text = task.strip().lower()

        task_type = "general"

        if any(keyword in text for keyword in self.WEBSITE_KEYWORDS):
            task_type = "website"

        elif any(keyword in text for keyword in self.SOFTWARE_KEYWORDS):
            task_type = "software"

        elif any(keyword in text for keyword in self.EXCEL_KEYWORDS):
            task_type = "excel"

        elif any(keyword in text for keyword in self.DATABASE_KEYWORDS):
            task_type = "database"

        return {
            "original_task": task.strip(),
            "task_type": task_type,
            "keywords": self._extract_keywords(text)
        }

    def _extract_keywords(self, text):

        keyword_groups = (
            self.SOFTWARE_KEYWORDS
            + self.WEBSITE_KEYWORDS
            + self.DATABASE_KEYWORDS
            + self.EXCEL_KEYWORDS
        )

        return [
            keyword
            for keyword in keyword_groups
            if keyword in text
        ]