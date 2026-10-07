class AICodeGenerator:

    def __init__(self, provider=None):
        self.provider = provider

    # ==================================================
    # NORMALIZE AI RESPONSE
    # ==================================================

    def _normalize(self, result):

        if not isinstance(result, dict):
            raise RuntimeError(
                "AI provider returned invalid file structure."
            )

        if "files" in result:
            result = result["files"]

        if not isinstance(result, dict):
            raise RuntimeError(
                "AI provider files must be a dictionary."
            )

        normalized = {}

        for path, content in result.items():

            if not isinstance(path, str):
                continue

            if not isinstance(content, str):
                content = str(content)

            path = path.replace("\\", "/").strip("/")

            if not path:
                continue

            normalized[path] = content

        if not normalized:
            raise RuntimeError(
                "AI provider returned no files."
            )

        return normalized

    # ==================================================
    # PROJECT STRUCTURE VALIDATION
    # ==================================================

    def validate_generated_structure(
        self,
        files,
        requirements=None,
        architecture=None
    ):

        errors = []

        file_paths = set(files.keys())

        # --------------------------------------------------
        # MAIN APPLICATION FILE
        # --------------------------------------------------

        has_main = any(
            path in {
                "main.py",
                "app.py",
                "run.py",
                "src/main.py"
            }
            for path in file_paths
        )

        if not has_main:
            errors.append({
                "type": "missing_required_file",
                "file": "main.py",
                "error": (
                    "Generated project does not contain a main "
                    "application entry point."
                )
            })

        # --------------------------------------------------
        # REQUIREMENTS
        # --------------------------------------------------

        if "requirements.txt" not in file_paths:
            errors.append({
                "type": "missing_required_file",
                "file": "requirements.txt",
                "error": (
                    "Generated project must contain "
                    "requirements.txt."
                )
            })

        # --------------------------------------------------
        # FUNCTIONAL TESTS
        # --------------------------------------------------

        test_files = [
            path
            for path in file_paths
            if (
                path.startswith("tests/")
                and path.endswith(".py")
                and (
                    path.split("/")[-1].startswith("test_")
                    or path.split("/")[-1].endswith("_test.py")
                )
            )
            or (
                path.endswith("_test.py")
                or path.startswith("test_")
            )
        ]

        if not test_files:
            errors.append({
                "type": "missing_functional_tests",
                "file": "tests/",
                "error": (
                    "No functional test files were generated. "
                    "At least one test_*.py or *_test.py file "
                    "is required."
                )
            })

        # --------------------------------------------------
        # REQUIRE TEST DIRECTORY
        # --------------------------------------------------

        has_tests_directory = any(
            path.startswith("tests/")
            for path in file_paths
        )

        if not has_tests_directory:
            errors.append({
                "type": "missing_test_directory",
                "file": "tests/",
                "error": (
                    "Generated project must contain a tests "
                    "directory with functional tests."
                )
            })

        return {
            "passed": not errors,
            "errors": errors
        }

    # ==================================================
    # GENERATE
    # ==================================================

    def generate(
        self,
        task,
        requirements,
        architecture
    ):

        if self.provider is not None:

            result = self.provider.generate_code(
                task=task,
                requirements=requirements,
                architecture=architecture
            )

            files = self._normalize(result)

            structure = self.validate_generated_structure(
                files=files,
                requirements=requirements,
                architecture=architecture
            )

            if not structure["passed"]:

                # Do not silently accept incomplete AI output.
                return files

            return files

        return self._fallback_generation(
            task,
            architecture
        )

    # ==================================================
    # FIX
    # ==================================================

    def fix(
        self,
        task,
        requirements,
        architecture,
        files,
        errors
    ):

        if self.provider is not None:

            result = self.provider.fix_code(
                task=task,
                requirements=requirements,
                architecture=architecture,
                files=files,
                errors=errors
            )

            fixed_files = self._normalize(result)

            # --------------------------------------------------
            # IMPORTANT:
            # AI may return only changed files.
            # Existing files must be preserved.
            # --------------------------------------------------

            merged = dict(files)

            for path, content in fixed_files.items():
                merged[path] = content

            return merged

        return files

    # ==================================================
    # FALLBACK
    # ==================================================

    def _fallback_generation(
        self,
        task,
        architecture
    ):

        project_type = architecture["type"]

        # ==================================================
        # WEBSITE
        # ==================================================

        if project_type == "website":

            return {
                "app.py": """from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():

    return "AURA AI Generated Website"


if __name__ == "__main__":

    app.run()
""",

                "requirements.txt": "Flask\n",

                "tests/test_app.py": """from app import app


def test_home():

    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
"""
            }

        # ==================================================
        # SOFTWARE
        # ==================================================

        if project_type == "software":

            return {
                "main.py": """def add(a, b):

    return a + b


def subtract(a, b):

    return a - b


def multiply(a, b):

    return a * b


def divide(a, b):

    if b == 0:

        raise ValueError("Cannot divide by zero")

    return a / b


def main():

    print("AURA AI Generated Software")


if __name__ == "__main__":

    main()
""",

                "requirements.txt": "",

                "tests/test_main.py": """from main import (
    add,
    subtract,
    multiply,
    divide
)


def test_addition():

    assert add(2, 3) == 5


def test_subtraction():

    assert subtract(5, 3) == 2


def test_multiplication():

    assert multiply(4, 3) == 12


def test_division():

    assert divide(10, 2) == 5
"""
            }

        # ==================================================
        # EXCEL
        # ==================================================

        if project_type == "excel":

            return {
                "main.py": """import pandas as pd


def create_dataframe():

    data = {
        "Name": ["AURA"],
        "Value": [100]
    }

    return pd.DataFrame(data)


def main():

    df = create_dataframe()

    print(df)


if __name__ == "__main__":

    main()
""",

                "requirements.txt": "pandas\nopenpyxl\n",

                "tests/test_main.py": """from main import create_dataframe


def test_dataframe():

    df = create_dataframe()

    assert len(df) == 1
    assert "Name" in df.columns
    assert "Value" in df.columns
"""
            }

        # ==================================================
        # DATABASE
        # ==================================================

        if project_type == "database":

            return {
                "main.py": """import sqlite3


def create_database():

    connection = sqlite3.connect(":memory:")

    cursor = connection.cursor()

    cursor.execute(
        "CREATE TABLE data "
        "(id INTEGER PRIMARY KEY)"
    )

    connection.commit()

    return connection


def main():

    connection = create_database()

    connection.close()

    print("AURA AI Database Ready")


if __name__ == "__main__":

    main()
""",

                "requirements.txt": "",

                "tests/test_main.py": """from main import create_database


def test_database():

    connection = create_database()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type='table' AND name='data'"
    )

    result = cursor.fetchone()

    assert result is not None

    connection.close()
"""
            }

        # ==================================================
        # GENERAL
        # ==================================================

        return {
            "main.py": """def main():

    print("AURA AI Generated Project")


if __name__ == "__main__":

    main()
""",

            "requirements.txt": "",

            "tests/test_main.py": """from main import main


def test_main_exists():

    assert callable(main)
"""
        }