class RequirementAnalyzer:

    def analyze(self, task):

        if not isinstance(task, str):
            raise ValueError(
                "Task must be a string."
            )

        task = task.strip()

        if not task:
            raise ValueError(
                "Development task is required."
            )

        text = task.lower()

        if any(
            word in text
            for word in [
                "website",
                "web app",
                "web application"
            ]
        ):
            project_type = "website"

        elif any(
            word in text
            for word in [
                "software",
                "application",
                "desktop app",
                "python app"
            ]
        ):
            project_type = "software"

        elif any(
            word in text
            for word in [
                "excel",
                "xlsx",
                "spreadsheet"
            ]
        ):
            project_type = "excel"

        elif any(
            word in text
            for word in [
                "database",
                "sqlite",
                "mysql",
                "postgres"
            ]
        ):
            project_type = "database"

        else:
            project_type = "general"

        return {
            "task": task,
            "project_type": project_type,
            "requirements": self._extract_requirements(
                text
            )
        }

    def _extract_requirements(self, text):

        requirements = []

        keyword_map = {
            "billing": "billing",
            "inventory": "inventory",
            "login": "authentication",
            "admin": "admin panel",
            "dashboard": "dashboard",
            "report": "reporting",
            "pdf": "PDF generation",
            "excel": "Excel processing",
            "database": "database"
        }

        for keyword, requirement in keyword_map.items():

            if keyword in text:
                requirements.append(
                    requirement
                )

        return requirements