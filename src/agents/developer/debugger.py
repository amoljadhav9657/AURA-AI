from pathlib import Path
import re


class Debugger:

    def __init__(self):
        print("🐛 AURA Debugger: READY")

    # =========================================================
    # ANALYZE ERROR
    # =========================================================

    def analyze_error(self, error_text):

        if not error_text or not error_text.strip():

            return {
                "success": False,
                "message": "No error provided."
            }

        error_text = error_text.strip()

        error_type = self.detect_error_type(
            error_text
        )

        file_path = self.extract_file(
            error_text
        )

        line_number = self.extract_line(
            error_text
        )

        message = self.extract_message(
            error_text
        )

        cause = self.detect_cause(
            error_type,
            message
        )

        suggestion = self.create_suggestion(
            error_type,
            message
        )

        return {
            "success": True,
            "error_type": error_type,
            "file": file_path,
            "line": line_number,
            "message": message,
            "possible_cause": cause,
            "suggestion": suggestion
        }

    # =========================================================
    # ERROR TYPE
    # =========================================================

    def detect_error_type(self, text):

        error_types = [
            "SyntaxError",
            "IndentationError",
            "ModuleNotFoundError",
            "ImportError",
            "NameError",
            "TypeError",
            "ValueError",
            "AttributeError",
            "FileNotFoundError",
            "PermissionError",
            "KeyError",
            "IndexError",
            "ZeroDivisionError",
            "TimeoutError"
        ]

        for error_type in error_types:

            if error_type in text:

                return error_type

        return "UnknownError"

    # =========================================================
    # FILE
    # =========================================================

    def extract_file(self, text):

        match = re.search(
            r'File ["\']([^"\']+)["\']',
            text
        )

        if match:

            return match.group(1)

        return None

    # =========================================================
    # LINE
    # =========================================================

    def extract_line(self, text):

        match = re.search(
            r'line (\d+)',
            text
        )

        if match:

            return int(
                match.group(1)
            )

        return None

    # =========================================================
    # MESSAGE
    # =========================================================

    def extract_message(self, text):

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        if not lines:

            return ""

        for line in reversed(lines):

            if (
                "Error" not in line
                and "Traceback" not in line
            ):

                return line

        return lines[-1]

    # =========================================================
    # POSSIBLE CAUSE
    # =========================================================

    def detect_cause(
        self,
        error_type,
        message
    ):

        causes = {

            "SyntaxError":
                "Python syntax is invalid.",

            "IndentationError":
                "Code indentation is incorrect.",

            "ModuleNotFoundError":
                "A required Python module is not installed or the import path is incorrect.",

            "ImportError":
                "A requested module or object could not be imported.",

            "NameError":
                "A variable, function, or class name is not defined.",

            "TypeError":
                "An operation received an incompatible data type.",

            "ValueError":
                "A function received an invalid value.",

            "AttributeError":
                "The requested object does not contain that attribute or method.",

            "FileNotFoundError":
                "The requested file or directory does not exist.",

            "PermissionError":
                "The application does not have permission to access the resource.",

            "KeyError":
                "The requested dictionary key does not exist.",

            "IndexError":
                "A list or sequence index is outside the valid range.",

            "ZeroDivisionError":
                "The program attempted to divide by zero.",

            "TimeoutError":
                "The operation took longer than the allowed time."
        }

        return causes.get(
            error_type,
            "The error requires further investigation."
        )

    # =========================================================
    # SUGGEST FIX
    # =========================================================

    def create_suggestion(
        self,
        error_type,
        message
    ):

        suggestions = {

            "SyntaxError":
                "Check brackets, quotes, colons, and Python syntax near the reported line.",

            "IndentationError":
                "Check spaces/tabs and make sure the code block is correctly indented.",

            "ModuleNotFoundError":
                "Check the import path and install the missing package inside the active virtual environment if required.",

            "ImportError":
                "Check the module name and verify that the requested class or function exists.",

            "NameError":
                "Check whether the variable, function, or class was defined before it was used.",

            "TypeError":
                "Check the data types of the values passed to the failing operation.",

            "ValueError":
                "Check the value supplied to the failing function.",

            "AttributeError":
                "Check the object's class and verify that the requested method or attribute exists.",

            "FileNotFoundError":
                "Check the file path and make sure the required file exists.",

            "PermissionError":
                "Check file permissions and whether another application is locking the resource.",

            "KeyError":
                "Check that the requested dictionary key exists before accessing it.",

            "IndexError":
                "Check the sequence length and make sure the index is within range.",

            "ZeroDivisionError":
                "Add validation so the divisor cannot be zero.",

            "TimeoutError":
                "Check the operation duration and timeout configuration."
        }

        return suggestions.get(
            error_type,
            "Inspect the traceback and reproduce the error for deeper analysis."
        )

    # =========================================================
    # DISPLAY REPORT
    # =========================================================

    def display_report(self, report):

        if not report.get("success"):

            print(
                "❌",
                report.get(
                    "message",
                    "Debugging failed."
                )
            )

            return

        print()
        print("🐛 DEBUG REPORT")
        print("==============================")

        print()
        print(
            "Error Type:",
            report["error_type"]
        )

        print(
            "File:",
            report["file"]
        )

        print(
            "Line:",
            report["line"]
        )

        print(
            "Message:",
            report["message"]
        )

        print()
        print(
            "Possible Cause:"
        )

        print(
            report["possible_cause"]
        )

        print()
        print(
            "Suggested Fix:"
        )

        print(
            report["suggestion"]
        )


# =============================================================
# TEST
# =============================================================

if __name__ == "__main__":

    print()
    print("======================================")
    print(" AURA DEBUGGER TEST")
    print("======================================")
    print()

    debugger = Debugger()

    test_errors = [

        '''Traceback (most recent call last):
  File "calculator.py", line 10, in <module>
    result = calculate()
SyntaxError: invalid syntax''',

        '''Traceback (most recent call last):
  File "main.py", line 5, in <module>
    import pandas
ModuleNotFoundError: No module named 'pandas' ''',

        '''Traceback (most recent call last):
  File "app.py", line 20, in <module>
    print(user.name)
AttributeError: 'NoneType' object has no attribute 'name' '''
    ]

    for error in test_errors:

        print()
        print("❌ ERROR INPUT")
        print("------------------------------")
        print(error)

        report = debugger.analyze_error(
            error
        )

        debugger.display_report(
            report
        )

        print()
        print("--------------------------------------")

    print()
    print("======================================")
    print(" ✅ DEBUGGER TEST COMPLETE")
    print("======================================")
