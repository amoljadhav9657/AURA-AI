from pathlib import Path

from .task_analyzer import TaskAnalyzer
from .project_planner import ProjectPlanner
from .code_generator import CodeGenerator
from .file_manager import FileManager
from .test_engine import TestEngine
from .debugger import Debugger


class DeveloperAgent:

    def __init__(self, workspace="workspace"):

        self.analyzer = TaskAnalyzer()
        self.planner = ProjectPlanner()
        self.generator = CodeGenerator()
        self.file_manager = FileManager(workspace)
        self.test_engine = TestEngine()
        self.debugger = Debugger()

    def create_project(
        self,
        task,
        project_name="aura_generated_project"
    ):

        # -----------------------------------------------------
        # STEP 1: ANALYZE
        # -----------------------------------------------------

        analysis = self.analyzer.analyze(task)

        # -----------------------------------------------------
        # STEP 2: PLAN
        # -----------------------------------------------------

        plan = self.planner.create_plan(
            analysis
        )

        # -----------------------------------------------------
        # STEP 3: CREATE PROJECT
        # -----------------------------------------------------

        project_path = self.file_manager.create_project(
            project_name
        )

        # -----------------------------------------------------
        # STEP 4: GENERATE CODE
        # -----------------------------------------------------

        generated_files = self.generator.generate_project(
            plan
        )

        created_files = []

        for relative_path, content in generated_files.items():

            file_path = self.file_manager.create_file(
                project_path,
                relative_path,
                content
            )

            created_files.append(
                str(
                    file_path.relative_to(project_path)
                )
            )

        # -----------------------------------------------------
        # STEP 5: TEST
        # -----------------------------------------------------

        validation = self.test_engine.validate(
            project_path
        )

        # -----------------------------------------------------
        # STEP 6: DEBUG ANALYSIS
        # -----------------------------------------------------

        debug_report = self.debugger.analyze(
            validation
        )

        return {
            "status": (
                "success"
                if validation["overall_passed"]
                else "needs_debugging"
            ),
            "task": task,
            "analysis": analysis,
            "plan": plan,
            "project_path": str(
                Path(project_path).resolve()
            ),
            "files": created_files,
            "validation": validation,
            "debug": debug_report
        }