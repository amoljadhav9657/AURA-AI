class Debugger:

    def analyze(self, validation):

        errors = []

        # ---------------------------------
        # 1. COMPILE ERRORS
        # ---------------------------------

        for result in validation.get(
            "compile_results",
            []
        ):

            if not result.get("passed", False):

                errors.append({
                    "type": "compile_error",
                    "file": result.get(
                        "file",
                        ""
                    ),
                    "error": result.get(
                        "stderr",
                        ""
                    )
                })

        # ---------------------------------
        # 2. FUNCTIONAL TEST ERRORS
        # ---------------------------------

        for result in validation.get(
            "test_results",
            []
        ):

            if not result.get("passed", False):

                errors.append({
                    "type": "functional_test_error",
                    "file": result.get(
                        "file",
                        ""
                    ),
                    "error": result.get(
                        "stderr",
                        ""
                    ),
                    "output": result.get(
                        "stdout",
                        ""
                    )
                })

        # ---------------------------------
        # 3. RUNTIME ERRORS
        # ---------------------------------

        for result in validation.get(
            "runtime_results",
            []
        ):

            if not result.get("passed", False):

                errors.append({
                    "type": "runtime_error",
                    "file": result.get(
                        "file",
                        ""
                    ),
                    "error": result.get(
                        "stderr",
                        ""
                    ),
                    "output": result.get(
                        "stdout",
                        ""
                    )
                })

        return {
            "has_errors": bool(errors),
            "errors": errors
        }

    # ---------------------------------
    # FIX REQUEST
    # ---------------------------------

    def build_fix_request(self, errors):

        if not errors:
            return None

        return {
            "instruction": (
                "Fix all reported software and "
                "functional testing errors. "
                "Preserve existing functionality. "
                "Do not weaken or remove tests "
                "just to make them pass."
            ),
            "errors": errors
        }

    # ---------------------------------
    # BACKWARD COMPATIBILITY
    # ---------------------------------

    def create_fix_request(self, errors):

        return self.build_fix_request(
            errors
        )