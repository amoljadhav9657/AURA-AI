class Architect:

    def design(self, analysis):

        task_type = analysis["task_type"]

        if task_type == "website":
            return {
                "type": "website",
                "stack": {
                    "backend": "Flask",
                    "frontend": "HTML/CSS/JavaScript",
                    "database": "SQLite"
                },
                "folders": [
                    "templates",
                    "static",
                    "tests"
                ]
            }

        if task_type == "software":
            return {
                "type": "software",
                "stack": {
                    "language": "Python",
                    "ui": "Tkinter",
                    "database": "SQLite"
                },
                "folders": [
                    "modules",
                    "tests"
                ]
            }

        if task_type == "excel":
            return {
                "type": "excel",
                "stack": {
                    "language": "Python",
                    "libraries": [
                        "pandas",
                        "openpyxl"
                    ]
                },
                "folders": [
                    "analysis",
                    "reports",
                    "tests"
                ]
            }

        if task_type == "database":
            return {
                "type": "database",
                "stack": {
                    "database": "SQLite"
                },
                "folders": [
                    "models",
                    "queries",
                    "tests"
                ]
            }

        return {
            "type": "general",
            "stack": {
                "language": "Python"
            },
            "folders": [
                "tests"
            ]
        }
