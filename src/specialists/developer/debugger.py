class Debugger:

    def analyze(self, validation_result):

        errors = []

        for result in validation_result.get(
            "compile_results",
            []
        ):

            if not result["passed"]:

                errors.append(
                    {
                        "file": result["file"],
                        "type": "compile_error",
                        "message": result["error"]
                    }
                )

        for result in validation_result.get(
            "test_results",
            []
        ):

            if not result["passed"]:

                errors.append(
                    {
                        "file": result["file"],
                        "type": "test_error",
                        "message": result["stderr"]
                    }
                )

        return {
            "has_errors": len(errors) > 0,
            "errors": errors
        }

    def suggest_fix(self, error):

        message = error.get(
            "message",
            ""
        ).lower()

        if "indentationerror" in message:
            return "Check Python indentation."

        if "modulenotfounderror" in message:
            return "Check imports and required dependencies."

        if "syntaxerror" in message:
            return "Check Python syntax."

        if "filenotfounderror" in message:
            return "Check file path and file creation."

        return "Inspect the error and modify the affected module."