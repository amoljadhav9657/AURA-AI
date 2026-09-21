from pathlib import Path


class FileManager:

    def __init__(self, workspace="workspace"):

        self.workspace = Path(workspace)
        self.workspace.mkdir(
            parents=True,
            exist_ok=True
        )

    def create_project(self, project_name):

        if not project_name:
            raise ValueError("Project name is required.")

        project_name = self._safe_name(project_name)

        project_path = self.workspace / project_name

        project_path.mkdir(
            parents=True,
            exist_ok=True
        )

        return project_path

    def create_file(
        self,
        project_path,
        relative_path,
        content=""
    ):

        project_path = Path(project_path)

        file_path = project_path / relative_path

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        file_path.write_text(
            content,
            encoding="utf-8"
        )

        return file_path

    def read_file(self, file_path):

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        return file_path.read_text(
            encoding="utf-8"
        )

    def list_files(self, project_path):

        project_path = Path(project_path)

        if not project_path.exists():
            return []

        return [
            str(path.relative_to(project_path))
            for path in project_path.rglob("*")
            if path.is_file()
        ]

    @staticmethod
    def _safe_name(name):

        allowed = (
            "abcdefghijklmnopqrstuvwxyz"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "0123456789"
            "_-"
        )

        cleaned = "".join(
            char if char in allowed else "_"
            for char in name.strip()
        )

        return cleaned.strip("_") or "aura_project"