class Debugger:

    def analyze(
        self,
        validation
    ):

        errors = []

        for result in validation.get(
            "compile_results",
            []
        ):

            if not result["passed"]:

                errors.append({
                    "file": result["file"],
                    "error": result["stderr"]
                })

        return {
            "has_errors": bool(errors),
            "errors": errors
        }

    def create_fix_request(
        self,
        errors
    ):

        if not errors:
            return None

        return {
            "instruction": (
                "Fix the generated code while "
                "preserving existing functionality."
            ),
            "errors": errors
        }