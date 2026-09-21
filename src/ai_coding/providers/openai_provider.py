import json
import os

from openai import OpenAI

from .base_provider import AIProvider


class OpenAIProvider(AIProvider):

    def __init__(
        self,
        model=None,
        api_key=None
    ):

        self.api_key = (
            api_key
            or os.getenv("OPENAI_API_KEY")
        )

        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY is not configured."
            )

        self.model = (
            model
            or os.getenv(
                "AURA_CODING_MODEL",
                "gpt-5.6-luna"
            )
        )

        self.client = OpenAI(
            api_key=self.api_key
        )

    def _request(self, prompt):

        response = self.client.responses.create(
            model=self.model,
            input=prompt
        )

        return response.output_text

    def _parse_json(self, text):

        text = text.strip()

        if text.startswith("```"):

            lines = text.splitlines()

            if lines and lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            text = "\n".join(lines)

        try:
            return json.loads(text)

        except json.JSONDecodeError as exc:

            raise ValueError(
                "AI returned invalid JSON."
            ) from exc

    def generate_code(
        self,
        task,
        requirements,
        architecture
    ):

        prompt = f"""
You are AURA AI Coding Brain.

Your job is to generate a complete software
project from the user's requirement.

USER TASK:
{task}

REQUIREMENTS:
{json.dumps(requirements, indent=2)}

ARCHITECTURE:
{json.dumps(architecture, indent=2)}

Return ONLY valid JSON.

The JSON must have this exact structure:

{{
    "files": {{
        "relative/path/file.py": "complete file content",
        "requirements.txt": "dependencies"
    }}
}}

Rules:

1. Generate complete files.
2. Never use placeholders such as TODO.
3. Never use markdown fences.
4. All paths must be relative to the project.
5. Do not generate absolute paths.
6. Python files must be syntactically valid.
7. Keep dependencies minimal.
8. Do not include explanations outside JSON.
"""

        output = self._request(prompt)

        result = self._parse_json(output)

        files = result.get("files")

        if not isinstance(files, dict):
            raise ValueError(
                "AI response does not contain valid files."
            )

        return files

    def fix_code(
        self,
        task,
        requirements,
        architecture,
        files,
        errors
    ):

        prompt = f"""
You are AURA AI Debugger.

The generated project failed validation.

USER TASK:
{task}

REQUIREMENTS:
{json.dumps(requirements, indent=2)}

ARCHITECTURE:
{json.dumps(architecture, indent=2)}

CURRENT FILES:
{json.dumps(files, indent=2)}

ERRORS:
{json.dumps(errors, indent=2)}

Fix the project.

Return ONLY valid JSON:

{{
    "files": {{
        "relative/path/file.py": "complete corrected file content"
    }}
}}

Rules:

1. Return complete corrected files.
2. Preserve working functionality.
3. Fix the reported errors.
4. Do not use markdown.
5. Do not use TODO placeholders.
6. Paths must remain relative.
7. Do not return explanations.
"""

        output = self._request(prompt)

        result = self._parse_json(output)

        fixed_files = result.get("files")

        if not isinstance(fixed_files, dict):
            raise ValueError(
                "AI debugger returned invalid files."
            )

        return fixed_files