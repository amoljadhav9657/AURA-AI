from pathlib import Path
import ast
import shutil
import re


class AutoRepairEngine:

    def __init__(self):
        print("🔧 AURA Auto Repair Engine: READY")

    # =========================================================
    # BACKUP
    # =========================================================

    def create_backup(self, project_path):

        project_path = Path(project_path)

        backup_path = project_path.parent / (
            project_path.name + "_backup"
        )

        try:

            if backup_path.exists():
                shutil.rmtree(backup_path)

            shutil.copytree(
                project_path,
                backup_path
            )

            print(
                "💾 BACKUP CREATED:",
                backup_path
            )

            return backup_path

        except Exception as exc:

            print(
                "❌ BACKUP FAILED:",
                exc
            )

            return None

    # =========================================================
    # ERROR CLASSIFICATION
    # =========================================================

    def classify_error(self, error_text):

        text = str(error_text)

        if "SyntaxError" in text:
            return "SyntaxError"

        if "IndentationError" in text:
            return "IndentationError"

        if "ModuleNotFoundError" in text:
            return "ModuleNotFoundError"

        if "ImportError" in text:
            return "ImportError"

        if "NameError" in text:
            return "NameError"

        if "AttributeError" in text:
            return "AttributeError"

        if "TypeError" in text:
            return "TypeError"

        if "FileNotFoundError" in text:
            return "FileNotFoundError"

        if "AssertionError" in text:
            return "AssertionError"

        return "UnknownError"

    # =========================================================
    # FIND FILE
    # =========================================================

    def find_error_file(
        self,
        project_path,
        error_text
    ):

        project_path = Path(project_path)

        match = re.search(
            r'File ["\']([^"\']+\.py)["\']',
            str(error_text)
        )

        if not match:
            return None

        file_name = Path(
            match.group(1)
        ).name

        matches = list(
            project_path.rglob(file_name)
        )

        if matches:
            return matches[0]

        return None

    # =========================================================
    # SYNTAX VALIDATION
    # =========================================================

    def validate_file(self, file_path):

        file_path = Path(file_path)

        try:

            source = file_path.read_text(
                encoding="utf-8"
            )

            ast.parse(source)

            return {
                "success": True,
                "file": str(file_path)
            }

        except SyntaxError as exc:

            return {
                "success": False,
                "file": str(file_path),
                "error": str(exc),
                "line": exc.lineno
            }

        except Exception as exc:

            return {
                "success": False,
                "file": str(file_path),
                "error": str(exc)
            }

    # =========================================================
    # SAFE SYNTAX REPAIR
    # =========================================================

    def repair_syntax(
        self,
        file_path,
        error_text
    ):

        file_path = Path(file_path)

        try:

            source = file_path.read_text(
                encoding="utf-8"
            )

            original = source

            # -------------------------------------------------
            # Remove accidental trailing whitespace
            # -------------------------------------------------

            lines = source.splitlines()

            cleaned_lines = [
                line.rstrip()
                for line in lines
            ]

            source = "\n".join(
                cleaned_lines
            ) + "\n"

            # -------------------------------------------------
            # Common accidental replacement
            # -------------------------------------------------

            source = source.replace(
                "\t",
                "    "
            )

            # -------------------------------------------------
            # Validate after safe cleanup
            # -------------------------------------------------

            try:

                ast.parse(source)

            except SyntaxError:

                # Safe cleanup could not fix it.
                # Do not overwrite original code.

                print(
                    "⚠️ Syntax requires deeper repair."
                )

                return {
                    "success": False,
                    "changed": False,
                    "reason":
                        "Automatic safe syntax repair was insufficient."
                }

            # -------------------------------------------------
            # Write only if changed
            # -------------------------------------------------

            if source != original:

                file_path.write_text(
                    source,
                    encoding="utf-8"
                )

                print(
                    "🔧 SAFE SYNTAX REPAIR APPLIED"
                )

                return {
                    "success": True,
                    "changed": True,
                    "file": str(file_path)
                }

            print(
                "ℹ️ No safe syntax changes required."
            )

            return {
                "success": True,
                "changed": False,
                "file": str(file_path)
            }

        except Exception as exc:

            print(
                "❌ SYNTAX REPAIR FAILED:",
                exc
            )

            return {
                "success": False,
                "changed": False,
                "error": str(exc)
            }

    # =========================================================
    # REPAIR
    # =========================================================

    def repair(
        self,
        project_path,
        error_text
    ):

        print()
        print(
            "======================================"
        )
        print(
            " 🔧 AURA AUTOMATIC REPAIR"
        )
        print(
            "======================================"
        )

        project_path = Path(
            project_path
        )

        if not project_path.exists():

            return {
                "success": False,
                "error":
                    "Project path does not exist."
            }

        error_type = self.classify_error(
            error_text
        )

        print()
        print(
            "🐛 ERROR TYPE:",
            error_type
        )

        # -----------------------------------------------------
        # BACKUP FIRST
        # -----------------------------------------------------

        backup = self.create_backup(
            project_path
        )

        if not backup:

            return {
                "success": False,
                "error":
                    "Backup could not be created."
            }

        # -----------------------------------------------------
        # FIND ERROR FILE
        # -----------------------------------------------------

        error_file = self.find_error_file(
            project_path,
            error_text
        )

        # -----------------------------------------------------
        # SYNTAX / INDENTATION
        # -----------------------------------------------------

        if error_type in {
            "SyntaxError",
            "IndentationError"
        }:

            if not error_file:

                return {
                    "success": False,
                    "error":
                        "Could not identify error file."
                }

            result = self.repair_syntax(
                error_file,
                error_text
            )

            result["backup"] = str(
                backup
            )

            return result

        # -----------------------------------------------------
        # UNSAFE ERRORS
        # -----------------------------------------------------

        print()
        print(
            "⚠️ ERROR REQUIRES DEEPER AI REPAIR"
        )

        print(
            "No risky automatic modification "
            "will be performed."
        )

        return {
            "success": False,
            "changed": False,
            "error_type": error_type,
            "backup": str(backup),
            "reason":
                "Safe repair rule not available."
        }

    # =========================================================
    # DISPLAY
    # =========================================================

    def display_result(self, result):

        print()
        print(
            "🔧 REPAIR RESULT"
        )
        print(
            "=============================="
        )

        print(
            "Success:",
            result.get(
                "success"
            )
        )

        print(
            "Changed:",
            result.get(
                "changed",
                False
            )
        )

        if result.get("file"):

            print(
                "File:",
                result["file"]
            )

        if result.get("backup"):

            print(
                "Backup:",
                result["backup"]
            )

        if result.get("reason"):

            print(
                "Reason:",
                result["reason"]
            )


# =============================================================
# TEST
# =============================================================

if __name__ == "__main__":

    print()
    print(
        "======================================"
    )
    print(
        " AURA AUTO REPAIR ENGINE TEST"
    )
    print(
        "======================================"
    )

    engine = AutoRepairEngine()

    test_project = Path(
        "workspace/auto_repair_test"
    )

    test_project.mkdir(
        parents=True,
        exist_ok=True
    )

    test_file = (
        test_project /
        "broken.py"
    )

    broken_code = """def hello()
    print("Hello from AURA")
"""

    test_file.write_text(
        broken_code,
        encoding="utf-8"
    )

    error_text = f'''Traceback (most recent call last):
  File "{test_file}", line 1
    def hello()
              ^
SyntaxError: expected ':'
'''

    print()
    print(
        "❌ BROKEN PROJECT CREATED"
    )

    result = engine.repair(
        test_project,
        error_text
    )

    engine.display_result(
        result
    )

    print()
    print(
        "======================================"
    )
    print(
        " ℹ️ AUTO REPAIR ENGINE TEST COMPLETE"
    )
    print(
        "======================================"
    )