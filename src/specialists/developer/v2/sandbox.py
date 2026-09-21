import subprocess
import sys
from pathlib import Path


class Sandbox:

    def __init__(self, timeout=30):
        self.timeout = timeout

    def compile(self, project_path):

        # Always convert to an absolute path.
        project_path = Path(
            project_path
        ).resolve()

        if not project_path.exists():
            return [{
                "file": "",
                "passed": False,
                "stderr": (
                    f"Project path does not exist: "
                    f"{project_path}"
                )
            }]

        results = []

        for file_path in project_path.rglob("*.py"):

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "py_compile",
                    str(file_path)
                ],
                cwd=str(project_path),
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            results.append({
                "file": str(
                    file_path.relative_to(
                        project_path
                    )
                ),
                "passed": result.returncode == 0,
                "stderr": result.stderr.strip()
            })

        return results

    def run_python_file(
        self,
        project_path,
        relative_file
    ):

        project_path = Path(
            project_path
        ).resolve()

        file_path = (
            project_path / relative_file
        ).resolve()

        # Security check:
        # file must remain inside project.
        try:
            file_path.relative_to(project_path)
        except ValueError:
            raise ValueError(
                "File path is outside the project."
            )

        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found: {relative_file}"
            )

        return subprocess.run(
            [
                sys.executable,
                str(file_path)
            ],
            cwd=str(project_path),
            capture_output=True,
            text=True,
            timeout=self.timeout
        )