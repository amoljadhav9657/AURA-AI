import os
import json
import time

from google import genai

from .base_provider import AIProvider


class GeminiRateLimitError(RuntimeError):
    """Raised when Gemini API rate limits or quota limits are reached."""


class GeminiProvider(AIProvider):

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = os.getenv(
            "AURA_GEMINI_MODEL",
            "gemini-3.8-flash"
        )

        self.max_retries = 3

    # ==================================================
    # RATE LIMIT DETECTION
    # ==================================================

    @staticmethod
    def _is_rate_limit_error(error):

        text = str(error).lower()

        return (
            "429" in text
            or "rate limit" in text
            or "too many requests" in text
            or "quota" in text
        )

    # ==================================================
    # DAILY QUOTA DETECTION
    # ==================================================

    @staticmethod
    def _is_daily_quota_error(error):

        text = str(error).lower()

        return (
            "per day" in text
            or "daily" in text
            or "daily quota" in text
            or "limit:" in text
        )

    # ==================================================
    # GEMINI REQUEST
    # ==================================================

    def _request(self, prompt):

        last_error = None

        for attempt in range(
            1,
            self.max_retries + 1
        ):

            try:

                interaction = (
                    self.client.interactions.create(
                        model=self.model,
                        input=prompt
                    )
                )

                text = interaction.output_text

                if not text:

                    raise RuntimeError(
                        "Gemini returned an empty response."
                    )

                return text.strip()

            except Exception as error:

                last_error = error

                # ==========================================
                # RATE LIMIT / QUOTA HANDLING
                # ==========================================

                if self._is_rate_limit_error(error):

                    print()
                    print("=" * 60)
                    print("AURA GEMINI RATE LIMIT")
                    print("=" * 60)
                    print(
                        f"Model: {self.model}"
                    )
                    print(
                        f"Attempt: {attempt}/{self.max_retries}"
                    )
                    print(
                        f"Error: {error}"
                    )

                    # --------------------------------------
                    # DAILY QUOTA
                    # --------------------------------------

                    if self._is_daily_quota_error(error):

                        print(
                            "Daily quota appears to be exhausted."
                        )

                        print(
                            "Stopping retries to avoid "
                            "wasting API requests."
                        )

                        print("=" * 60)

                        raise GeminiRateLimitError(
                            "Gemini daily quota/rate limit "
                            f"was reached for model '{self.model}'. "
                            "No additional retry was attempted."
                        ) from error

                    # --------------------------------------
                    # TEMPORARY RATE LIMIT
                    # --------------------------------------

                    if attempt < self.max_retries:

                        wait_seconds = 60

                        print(
                            f"Temporary rate limit detected. "
                            f"Waiting {wait_seconds} seconds..."
                        )

                        time.sleep(
                            wait_seconds
                        )

                        continue

                    print("=" * 60)

                    raise GeminiRateLimitError(
                        "Gemini rate limit remained active "
                        f"after {self.max_retries} attempts."
                    ) from error

                # ==========================================
                # OTHER ERRORS
                # ==========================================

                print(
                    f"[Gemini] Request failed "
                    f"(attempt {attempt}/"
                    f"{self.max_retries}): "
                    f"{error}"
                )

                if attempt < self.max_retries:

                    time.sleep(
                        2 ** (attempt - 1)
                    )

        raise RuntimeError(
            "Gemini request failed after "
            f"{self.max_retries} attempts: "
            f"{last_error}"
        )

    # ==================================================
    # JSON PARSER
    # ==================================================

    def _parse_json(self, text):

        text = text.strip()

        if text.startswith("```"):

            lines = text.splitlines()

            lines = lines[1:]

            if (
                lines
                and lines[-1].strip() == "```"
            ):

                lines = lines[:-1]

            text = "\n".join(
                lines
            ).strip()

        try:

            result = json.loads(
                text
            )

        except json.JSONDecodeError as error:

            raise RuntimeError(
                "Gemini returned invalid JSON.\n\n"
                f"Response:\n{text}\n\n"
                f"JSON Error:\n{error}"
            )

        if not isinstance(result, dict):

            raise RuntimeError(
                "Gemini response must be a JSON object."
            )

        return result

    # ==================================================
    # FILE VALIDATION
    # ==================================================

    def _validate_files(self, result):

        if "files" in result:

            files = result["files"]

        else:

            files = result

        if not isinstance(files, dict):

            raise RuntimeError(
                "Gemini did not return a valid files dictionary."
            )

        normalized = {}

        for path, content in files.items():

            if not isinstance(path, str):

                continue

            if not isinstance(content, str):

                content = str(content)

            normalized[path] = content

        if not normalized:

            raise RuntimeError(
                "Gemini returned no files."
            )

        return normalized

    # ==================================================
    # TEST DETECTION
    # ==================================================

    def _has_tests(self, files):

        for path in files:

            normalized = path.replace(
                "\\",
                "/"
            ).lower()

            filename = normalized.split("/")[-1]

            if (
                filename.startswith("test_")
                and filename.endswith(".py")
            ):

                return True

            if (
                filename.endswith("_test.py")
            ):

                return True

            if (
                normalized.startswith("tests/")
                and filename.endswith(".py")
            ):

                return True

        return False

    # ==================================================
    # CODE GENERATION
    # ==================================================

    def generate_code(
        self,
        task,
        requirements,
        architecture
    ):

        prompt = f"""
You are AURA AI Coding Brain.

You are an AUTONOMOUS SENIOR SOFTWARE ENGINEER.

Your job is to generate a COMPLETE,
EXECUTABLE and TESTED software project.

==================================================
USER TASK
==================================================

{task}

==================================================
REQUIREMENTS
==================================================

{json.dumps(
    requirements,
    indent=2
)}

==================================================
ARCHITECTURE
==================================================

{json.dumps(
    architecture,
    indent=2
)}

==================================================
MANDATORY OUTPUT
==================================================

You MUST return ALL required project files.

For a Python application, you MUST return:

1. Application source code.
2. requirements.txt
3. At least ONE automated functional test file.

Example:

{{
    "files": {{
        "main.py": "...",
        "requirements.txt": "...",
        "tests/test_main.py": "..."
    }}
}}

==================================================
CRITICAL TEST REQUIREMENT
==================================================

THIS IS MANDATORY.

You MUST create a real functional test file.

The test file MUST NOT be omitted.

The test file MUST test the ACTUAL USER REQUIREMENTS.

Do not create fake tests.

Do not only test application startup.

Do not only test that functions exist.

Tests must execute actual functionality.

==================================================
APPLICATION DESIGN
==================================================

Design the application so its functionality
can be imported and tested.

Avoid putting all business logic inside
an untestable interactive loop.

==================================================
STRICT RULES
==================================================

1. Return ONLY valid JSON.
2. Do NOT return markdown.
3. Do NOT use code fences.
4. Every file must contain COMPLETE code.
5. Do NOT return pseudo-code.
6. Do NOT return TODO placeholders.
7. Do NOT omit required files.
8. ALWAYS include requirements.txt.
9. ALWAYS include automated functional tests.
10. Tests MUST verify actual functionality.
11. Use relative project paths only.
12. Python files must compile.
13. Imports must be valid.
14. Tests must be executable with pytest.
15. Do not weaken requirements.
16. Do not create fake tests.
17. Do not only test application startup.
18. The generated project must be genuinely functional.

==================================================
FINAL FILE REQUIREMENT
==================================================

Before returning your answer, internally verify:

- main application exists
- requirements.txt exists
- test file exists
- tests verify requested functionality
- Python syntax is valid
- imports are valid

If any of these are missing, FIX them before returning.

Return ONLY the final JSON.
"""

        response = self._request(
            prompt
        )

        result = self._parse_json(
            response
        )

        files = self._validate_files(
            result
        )

        if not self._has_tests(files):

            raise RuntimeError(
                "AI generated project without "
                "mandatory functional tests."
            )

        return {
            "files": files
        }

    # ==================================================
    # CODE FIXING
    # ==================================================

    def fix_code(
        self,
        task,
        requirements,
        architecture,
        files,
        errors
    ):

        prompt = f"""
You are AURA AI Coding Brain.

You are an AUTONOMOUS SOFTWARE DEBUGGING
AND SOFTWARE TESTING ENGINEER.

The previous generated project failed validation.

You MUST repair the project.

==================================================
USER TASK
==================================================

{task}

==================================================
REQUIREMENTS
==================================================

{json.dumps(
    requirements,
    indent=2
)}

==================================================
ARCHITECTURE
==================================================

{json.dumps(
    architecture,
    indent=2
)}

==================================================
CURRENT PROJECT FILES
==================================================

{json.dumps(
    files,
    indent=2
)}

==================================================
DETECTED ERRORS
==================================================

{json.dumps(
    errors,
    indent=2
)}

==================================================
REPAIR REQUIREMENT
==================================================

Repair ALL detected errors.

If functional tests are missing,
CREATE functional pytest tests.

Tests must verify the actual user requirements.

Do NOT create fake tests.

Do NOT only test that functions exist.

Do NOT only test application startup.

Preserve existing functionality.

==================================================
FINAL PROJECT
==================================================

The final project MUST contain:

1. Complete application code.
2. requirements.txt
3. Functional pytest tests.

==================================================
OUTPUT FORMAT
==================================================

Return ONLY valid JSON:

{{
    "files": {{
        "main.py": "complete code",
        "requirements.txt": "dependencies",
        "tests/test_main.py": "complete functional tests"
    }}
}}

==================================================
STRICT RULES
==================================================

1. Return ONLY valid JSON.
2. No markdown.
3. No code fences.
4. Return COMPLETE files.
5. Preserve existing functionality.
6. Fix ALL detected errors.
7. ADD missing functional tests.
8. Tests must verify actual functionality.
9. Do NOT remove tests.
10. Do NOT weaken tests.
11. Do NOT return pseudo-code.
12. Do NOT return TODO placeholders.
13. Python code must compile.
14. Tests must run using pytest.
15. Imports must be valid.
16. Use relative paths.
17. Always include requirements.txt.
18. Always include at least one functional test file.

Return ONLY final JSON.
"""

        response = self._request(
            prompt
        )

        result = self._parse_json(
            response
        )

        files = self._validate_files(
            result
        )

        if not self._has_tests(files):

            raise RuntimeError(
                "AI repair failed to generate "
                "mandatory functional tests."
            )

        return {
            "files": files
        }