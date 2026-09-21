from pathlib import Path


class ProjectBuilder:

    def __init__(self, workspace):

        self.workspace = Path(
            workspace
        ).resolve()

        self.workspace.mkdir(
            parents=True,
            exist_ok=True
        )

    def create_project(
        self,
        project_name
    ):

        safe_name = self._safe_name(
            project_name
        )

        project_path = (
            self.workspace / safe_name
        )

        project_path.mkdir(
            parents=True,
            exist_ok=True
        )

        return project_path

    def build(
        self,
        project_path,
        files
    ):

        project_path = Path(
            project_path
        ).resolve()

        created = []

        for relative_path, content in files.items():

            file_path = (
                project_path / relative_path
            ).resolve()

            try:
                file_path.relative_to(
                    project_path
                )

            except ValueError:

                raise ValueError(
                    "Generated file is outside project."
                )

            file_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            file_path.write_text(
                content,
                encoding="utf-8"
            )

            created.append(
                str(
                    file_path.relative_to(
                        project_path
                    )
                )
            )

        return created

    @staticmethod
    def _safe_name(name):

        allowed = (
            "abcdefghijklmnopqrstuvwxyz"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "0123456789_-"
        )

        result = "".join(
            c if c in allowed else "_"
            for c in str(name).strip()
        )

        return (
            result.strip("_")
            or "aura_project"
        )