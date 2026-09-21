from pathlib import Path


class GenericProjectBuilder:

    def __init__(self, workspace="workspace"):

        self.workspace = Path(workspace)

        self.workspace.mkdir(
            parents=True,
            exist_ok=True
        )

        print("🏗️ Generic Project Builder: READY")

    # =========================================================
    # CREATE PROJECT
    # =========================================================

    def create_project(
        self,
        project_name,
        files
    ):

        if not project_name or not project_name.strip():

            return {
                "success": False,
                "message": "Project name is required."
            }

        if not files:

            return {
                "success": False,
                "message": "No files provided."
            }

        project_path = (
            self.workspace /
            project_name.strip()
        )

        project_path.mkdir(
            parents=True,
            exist_ok=True
        )

        created_files = []

        for file_name in files:

            relative_path = Path(file_name)

            file_path = (
                project_path /
                relative_path
            )

            file_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            if not file_path.exists():

                file_path.write_text(
                    "",
                    encoding="utf-8"
                )

            created_files.append(
                str(file_path)
            )

        return {
            "success": True,
            "project": str(
                project_path.resolve()
            ),
            "files": created_files
        }

    # =========================================================
    # WRITE FILE
    # =========================================================

    def write_file(
        self,
        project_path,
        file_name,
        content
    ):

        project_path = Path(
            project_path
        ).resolve()

        target_path = (
            project_path /
            Path(file_name)
        ).resolve()

        # -----------------------------------------------------
        # SECURITY
        # Prevent writing outside project directory.
        # -----------------------------------------------------

        try:

            target_path.relative_to(
                project_path
            )

        except ValueError:

            return {
                "success": False,
                "message":
                    "Unsafe file path rejected."
            }

        target_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        target_path.write_text(
            content,
            encoding="utf-8"
        )

        return {
            "success": True,
            "file": str(target_path)
        }

    # =========================================================
    # WRITE MULTIPLE FILES
    # =========================================================

    def write_files(
        self,
        project_path,
        file_contents
    ):

        results = []

        for file_name, content in (
            file_contents.items()
        ):

            result = self.write_file(
                project_path,
                file_name,
                content
            )

            results.append(
                result
            )

        failed = [
            result
            for result in results
            if not result.get("success")
        ]

        return {
            "success": not failed,
            "results": results
        }

    # =========================================================
    # LIST PROJECT FILES
    # =========================================================

    def list_project_files(
        self,
        project_path
    ):

        project_path = Path(
            project_path
        )

        if not project_path.exists():

            return []

        files = []

        for path in project_path.rglob("*"):

            if path.is_file():

                files.append(
                    str(
                        path.relative_to(
                            project_path
                        )
                    )
                )

        return sorted(files)

    # =========================================================
    # DISPLAY PROJECT
    # =========================================================

    def display_project(
        self,
        project_path
    ):

        files = self.list_project_files(
            project_path
        )

        print()
        print("📁 PROJECT:")
        print(
            Path(project_path).resolve()
        )

        print()
        print("📄 CREATED FILES:")

        if not files:

            print("   └── No files")

            return

        for file_name in files:

            print(
                "   └──",
                file_name
            )


# =============================================================
# TEST
# =============================================================

if __name__ == "__main__":

    print()
    print("======================================")
    print(" AURA GENERIC PROJECT BUILDER TEST")
    print("======================================")
    print()

    builder = GenericProjectBuilder()

    project_name = (
        "aura_generic_test"
    )

    files = [

        "main.py",

        "config.py",

        "database.py",

        "README.md",

        "src/app.py",

        "src/utils.py",

        "tests/test_main.py"
    ]

    print("🏗️ Creating project...")

    result = builder.create_project(
        project_name,
        files
    )

    if not result.get("success"):

        print(
            "❌ PROJECT CREATION FAILED"
        )

        print(
            result.get("message")
        )

    else:

        print(
            "✅ PROJECT CREATED"
        )

        project_path = result[
            "project"
        ]

        # -----------------------------------------------------
        # Write sample code
        # -----------------------------------------------------

        file_contents = {

            "main.py":
                '''def main():

    print("AURA Generic Project")


if __name__ == "__main__":
    main()
''',

            "config.py":
                '''APP_NAME = "AURA Generic Project"
''',

            "src/app.py":
                '''def run():

    return "Application running."
''',

            "src/utils.py":
                '''def add(a, b):

    return a + b
''',

            "tests/test_main.py":
                '''def test_basic():

    assert 1 + 1 == 2
''',

            "README.md":
                '''# AURA Generic Project

This project was created by the AURA Generic Project Builder.
'''
        }

        print()
        print("💻 WRITING PROJECT FILES...")

        write_result = builder.write_files(
            project_path,
            file_contents
        )

        if write_result.get("success"):

            print(
                "✅ FILES WRITTEN SUCCESSFULLY"
            )

        else:

            print(
                "❌ SOME FILES FAILED"
            )

        # -----------------------------------------------------
        # Display
        # -----------------------------------------------------

        builder.display_project(
            project_path
        )

    print()
    print("======================================")
    print(" ✅ GENERIC PROJECT BUILDER TEST COMPLETE")
    print("======================================")
