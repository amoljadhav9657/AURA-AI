class ProjectPlanner:

    def create_plan(self, analysis):

        task_type = analysis["task_type"]
        task = analysis["original_task"]

        if task_type == "website":

            return {
                "project_type": "website",
                "technology": {
                    "backend": "Flask",
                    "frontend": "HTML/CSS/JavaScript",
                    "database": "SQLite"
                },
                "modules": [
                    "application",
                    "templates",
                    "static",
                    "database",
                    "tests"
                ],
                "task": task
            }

        if task_type == "software":

            return {
                "project_type": "software",
                "technology": {
                    "language": "Python",
                    "database": "SQLite",
                    "ui": "Tkinter"
                },
                "modules": [
                    "application",
                    "database",
                    "modules",
                    "tests"
                ],
                "task": task
            }

        if task_type == "excel":

            return {
                "project_type": "excel",
                "technology": {
                    "language": "Python",
                    "libraries": [
                        "pandas",
                        "openpyxl"
                    ]
                },
                "modules": [
                    "data_processing",
                    "analysis",
                    "reports",
                    "tests"
                ],
                "task": task
            }

        if task_type == "database":

            return {
                "project_type": "database",
                "technology": {
                    "database": "SQLite"
                },
                "modules": [
                    "database",
                    "models",
                    "queries",
                    "tests"
                ],
                "task": task
            }

        return {
            "project_type": "general",
            "technology": {
                "language": "Python"
            },
            "modules": [
                "application",
                "tests"
            ],
            "task": task
        }