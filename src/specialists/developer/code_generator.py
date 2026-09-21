class CodeGenerator:

    def generate_project(self, plan):

        project_type = plan["project_type"]

        if project_type == "website":
            return self._website_template(plan)

        if project_type == "software":
            return self._software_template(plan)

        if project_type == "excel":
            return self._excel_template(plan)

        if project_type == "database":
            return self._database_template(plan)

        return self._general_template(plan)

    def _website_template(self, plan):

        return {
            "app.py": """from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "AURA Website"


if __name__ == "__main__":
    app.run(debug=True)
""",

            "templates/index.html": """<!DOCTYPE html>
<html>
<head>
    <title>AURA Website</title>
</head>
<body>

<h1>AURA Generated Website</h1>

<p>Website created by AURA Specialist Developer.</p>

</body>
</html>
""",

            "requirements.txt": "Flask\n"
        }

    def _software_template(self, plan):

        return {
            "main.py": """def main():
    print("AURA Generated Software")


if __name__ == "__main__":
    main()
""",

            "requirements.txt": ""
        }

    def _excel_template(self, plan):

        return {
            "main.py": """import pandas as pd


def analyze_excel(file_path):

    dataframe = pd.read_excel(file_path)

    print(dataframe.head())

    return dataframe


if __name__ == "__main__":
    print("AURA Excel Analyzer")
""",

            "requirements.txt": "pandas\nopenpyxl\n"
        }

    def _database_template(self, plan):

        return {
            "database.py": """import sqlite3


def connect():

    return sqlite3.connect("database.db")


if __name__ == "__main__":
    connection = connect()
    print("Database connected successfully.")
    connection.close()
""",

            "requirements.txt": ""
        }

    def _general_template(self, plan):

        return {
            "main.py": """def main():
    print("AURA Generated Project")


if __name__ == "__main__":
    main()
""",

            "requirements.txt": ""
        }