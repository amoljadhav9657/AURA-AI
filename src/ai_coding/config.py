from pathlib import Path


class CodingConfig:

    def __init__(
        self,
        workspace="workspace",
        timeout=30,
        max_iterations=3
    ):

        self.workspace = Path(workspace).resolve()

        self.timeout = timeout

        self.max_iterations = max_iterations

        self.workspace.mkdir(
            parents=True,
            exist_ok=True
        )