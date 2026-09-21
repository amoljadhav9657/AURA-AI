class Architect:

    def design(self, analysis):

        project_type = analysis[
            "project_type"
        ]

        if project_type == "website":

            return {
                "project_type": "website",

                "stack": {
                    "backend": "Flask",
                    "frontend": [
                        "HTML",
                        "CSS",
                        "JavaScript"
                    ],
                    "database": "SQLite"
                },

                "folders": [
                    "templates",
                    "static",
                    "tests"
                ]
            }

        if project_type == "software":

            return {
                "project_type": "software",

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

        if project_type == "excel":

            return {
                "project_type": "excel",

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

        if project_type == "database":

            return {
                "project_type": "database",

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
            "project_type": "general",

            "stack": {
                "language": "Python"
            },

            "folders": [
                "tests"
            ]
        }