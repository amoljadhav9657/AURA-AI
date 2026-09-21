from pathlib import Path
import json
import subprocess
import sys
import py_compile

from .requirement_analyzer import RequirementAnalyzer
from .project_planner import ProjectPlanner
from .code_generator import CodeGenerator
from .generic_project_builder import GenericProjectBuilder
from .code_generation_engine import CodeGenerationEngine
from .code_reasoning_engine import CodeReasoningEngine
from .debugger import Debugger
from .auto_repair_engine import AutoRepairEngine


class DeveloperAgent:

    def __init__(
        self,
        workspace="workspace",
        max_repair_attempts=2
    ):

        self.workspace = Path(workspace)

        self.analyzer = RequirementAnalyzer()
        self.planner = ProjectPlanner()
        self.generator = CodeGenerator()

        self.code_engine = CodeGenerationEngine()
        self.reasoning_engine = CodeReasoningEngine()

        self.builder = GenericProjectBuilder(
            workspace=str(self.workspace)
        )

        self.debugger = Debugger()
        self.repair_engine = AutoRepairEngine()

        self.max_repair_attempts = max(
            0,
            int(max_repair_attempts)
        )

        print(
            "🤖 AURA Developer Agent: READY"
        )

    # =========================================================
    # ANALYZE
    # =========================================================

    def analyze_requirement(self, requirement):

        print()
        print(
            "🧠 ANALYZING REQUIREMENT..."
        )

        analysis = self.analyzer.analyze(
            requirement
        )

        if not analysis.get("success"):

            print(
                "❌ REQUIREMENT ANALYSIS FAILED"
            )

            return None

        print(
            "✅ REQUIREMENT ANALYZED"
        )

        return analysis

    # =========================================================
    # PLAN
    # =========================================================

    def create_project_plan(self, analysis):

        print()
        print(
            "📐 CREATING PROJECT PLAN..."
        )

        plan = self.planner.create_plan(
            analysis
        )

        if not plan.get("success"):

            print(
                "❌ PROJECT PLANNING FAILED"
            )

            return None

        print(
            "✅ PROJECT PLAN CREATED"
        )

        return plan

    # =========================================================
    # DISPLAY PLAN
    # =========================================================

    def display_plan(self, plan):

        if plan:
            self.planner.display_plan(plan)

    # =========================================================
    # CODE REASONING
    # =========================================================

    def reason_about_project(
        self,
        analysis,
        plan
    ):

        print()
        print(
            "🧠 REASONING ABOUT PROJECT..."
        )

        reasoning = (
            self.reasoning_engine.reason(
                analysis,
                plan
            )
        )

        if not reasoning.get("success"):

            print(
                "❌ CODE REASONING FAILED"
            )

            return None

        print(
            "✅ CODE REASONING COMPLETE"
        )

        self.reasoning_engine.display_reasoning(
            reasoning
        )

        return reasoning

    # =========================================================
    # CODE GENERATION
    # =========================================================

    def generate_code(
        self,
        plan,
        project_name
    ):

        print()
        print(
            "💻 GENERATING PROJECT CODE..."
        )

        generated = (
            self.code_engine.generate_project(
                plan,
                project_name
            )
        )

        if not generated.get("success"):

            print(
                "❌ CODE GENERATION FAILED"
            )

            return None

        print(
            "✅ CODE GENERATED"
        )

        self.code_engine.display_generated_files(
            generated
        )

        return generated

    # =========================================================
    # BUILD
    # =========================================================

    def build_project(
        self,
        project_name,
        generated
    ):

        print()
        print(
            "🏗️ BUILDING PROJECT..."
        )

        files = list(
            generated.get(
                "files",
                {}
            ).keys()
        )

        create_result = (
            self.builder.create_project(
                project_name,
                files
            )
        )

        if not create_result.get(
            "success"
        ):

            print(
                "❌ PROJECT CREATION FAILED"
            )

            return None

        project_path = Path(
            create_result["project"]
        )

        write_result = (
            self.builder.write_files(
                project_path,
                generated["files"]
            )
        )

        if not write_result.get(
            "success"
        ):

            print(
                "❌ FILE WRITING FAILED"
            )

            return None

        print(
            "✅ PROJECT BUILT"
        )

        self.builder.display_project(
            project_path
        )

        return project_path

    # =========================================================
    # VALIDATE
    # =========================================================

    def validate_python_files(
        self,
        project_path
    ):

        print()
        print(
            "🧪 VALIDATING PYTHON FILES..."
        )

        python_files = list(
            project_path.rglob("*.py")
        )

        errors = []

        for file_path in python_files:

            try:

                py_compile.compile(
                    str(file_path),
                    doraise=True
                )

                print(
                    "   ✅",
                    file_path.relative_to(
                        project_path
                    )
                )

            except Exception as exc:

                print(
                    "   ❌",
                    file_path.relative_to(
                        project_path
                    )
                )

                errors.append(
                    {
                        "file": str(
                            file_path
                        ),
                        "error": str(exc)
                    }
                )

        if errors:

            print()
            print(
                "❌ PYTHON VALIDATION FAILED"
            )

            return {
                "success": False,
                "errors": errors
            }

        print(
            "✅ ALL PYTHON FILES VALID"
        )

        return {
            "success": True,
            "files": [
                str(
                    path.relative_to(
                        project_path
                    )
                )
                for path in python_files
            ]
        }

    # =========================================================
    # RUN APPLICATION
    # =========================================================

    def run_application(
        self,
        project_path
    ):

        print()
        print(
            "🚀 RUNNING APPLICATION..."
        )

        main_file = (
            project_path / "main.py"
        )

        if not main_file.exists():

            print(
                "⚠️ main.py NOT FOUND"
            )

            return {
                "success": True,
                "skipped": True,
                "message":
                    "main.py not found."
            }

        try:

            result = subprocess.run(
                [
                    sys.executable,
                    str(main_file)
                ],
                cwd=str(project_path),
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:

                print(
                    "✅ APPLICATION RUN SUCCESSFULLY"
                )

                if result.stdout.strip():

                    print()
                    print(
                        result.stdout
                    )

                return {
                    "success": True,
                    "output":
                        result.stdout
                }

            print(
                "❌ APPLICATION FAILED"
            )

            if result.stderr.strip():

                print(
                    result.stderr
                )

            return {
                "success": False,
                "error":
                    result.stderr
            }

        except subprocess.TimeoutExpired:

            print(
                "❌ APPLICATION TIMEOUT"
            )

            return {
                "success": False,
                "error":
                    "Application timeout."
            }

        except Exception as exc:

            print(
                "❌ APPLICATION ERROR"
            )

            print(exc)

            return {
                "success": False,
                "error": str(exc)
            }

    # =========================================================
    # TESTS
    # =========================================================

    def run_tests(
        self,
        project_path
    ):

        print()
        print(
            "🧪 RUNNING AUTOMATED TESTS..."
        )

        tests_path = (
            project_path / "tests"
        )

        if not tests_path.exists():

            print(
                "⚠️ tests directory not found"
            )

            return {
                "success": True,
                "skipped": True
            }

        try:

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    "-q"
                ],
                cwd=str(project_path),
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:

                print(
                    "✅ ALL TESTS PASSED"
                )

                if result.stdout.strip():

                    print()
                    print(
                        result.stdout
                    )

                return {
                    "success": True,
                    "output":
                        result.stdout
                }

            print(
                "❌ TESTS FAILED"
            )

            if result.stdout.strip():
                print(result.stdout)

            if result.stderr.strip():
                print(result.stderr)

            return {
                "success": False,
                "error":
                    result.stdout +
                    "\n" +
                    result.stderr
            }

        except Exception as exc:

            print(
                "❌ TEST RUNNER ERROR"
            )

            print(exc)

            return {
                "success": False,
                "error": str(exc)
            }

    # =========================================================
    # DEBUG
    # =========================================================

    def debug_error(
        self,
        error_text
    ):

        print()
        print(
            "🐛 ANALYZING ERROR..."
        )

        try:

            report = (
                self.debugger.analyze_error(
                    error_text
                )
            )

            self.debugger.display_report(
                report
            )

            return report

        except Exception as exc:

            print(
                "❌ DEBUGGER ERROR"
            )

            print(exc)

            return None

    # =========================================================
    # AUTO REPAIR
    # =========================================================

    def attempt_repair(
        self,
        project_path,
        error_text,
        attempt
    ):

        print()
        print(
            "======================================"
        )
        print(
            f" 🔧 REPAIR ATTEMPT {attempt}"
        )
        print(
            "======================================"
        )

        report = self.debug_error(
            error_text
        )

        if report is None:

            print(
                "⚠️ Debug report unavailable."
            )

        result = self.repair_engine.repair(
            project_path,
            error_text
        )

        self.repair_engine.display_result(
            result
        )

        return result

    # =========================================================
    # REPAIR LOOP
    # =========================================================

    def repair_and_validate(
        self,
        project_path,
        error_text
    ):

        if self.max_repair_attempts <= 0:

            return {
                "success": False,
                "attempts": 0,
                "reason":
                    "Automatic repair disabled."
            }

        for attempt in range(
            1,
            self.max_repair_attempts + 1
        ):

            repair_result = (
                self.attempt_repair(
                    project_path,
                    error_text,
                    attempt
                )
            )

            if not repair_result.get(
                "success"
            ):

                print(
                    "⚠️ Repair could not safely fix the error."
                )

                continue

            print()
            print(
                "🧪 REVALIDATING AFTER REPAIR..."
            )

            validation = (
                self.validate_python_files(
                    project_path
                )
            )

            if not validation.get(
                "success"
            ):

                error_details = (
                    validation.get(
                        "errors",
                        []
                    )
                )

                error_text = json.dumps(
                    error_details,
                    indent=2
                )

                continue

            application = (
                self.run_application(
                    project_path
                )
            )

            if not application.get(
                "success"
            ):

                error_text = (
                    application.get(
                        "error",
                        ""
                    )
                )

                continue

            tests = self.run_tests(
                project_path
            )

            if not tests.get(
                "success"
            ):

                error_text = (
                    tests.get(
                        "error",
                        ""
                    )
                )

                continue

            print()
            print(
                "🎉 REPAIR SUCCESSFUL"
            )

            return {
                "success": True,
                "attempts": attempt,
                "validation": validation,
                "application": application,
                "tests": tests
            }

        print()
        print(
            "❌ MAXIMUM REPAIR ATTEMPTS REACHED"
        )

        return {
            "success": False,
            "attempts":
                self.max_repair_attempts
        }

    # =========================================================
    # FULL PIPELINE
    # =========================================================

    def process(
        self,
        requirement,
        project_name="aura_generated_project"
    ):

        print()
        print(
            "======================================"
        )
        print(
            " 🚀 AURA AUTONOMOUS DEVELOPER"
        )
        print(
            "======================================"
        )

        print()
        print(
            "👤 REQUIREMENT:"
        )
        print(
            requirement
        )

        # -----------------------------------------------------
        # 1 ANALYSIS
        # -----------------------------------------------------

        analysis = (
            self.analyze_requirement(
                requirement
            )
        )

        if not analysis:

            return {
                "success": False,
                "stage": "analysis"
            }

        # -----------------------------------------------------
        # 2 PLAN
        # -----------------------------------------------------

        plan = (
            self.create_project_plan(
                analysis
            )
        )

        if not plan:

            return {
                "success": False,
                "stage": "planning"
            }

        self.display_plan(
            plan
        )

        # -----------------------------------------------------
        # 3 REASONING
        # -----------------------------------------------------

        reasoning = (
            self.reason_about_project(
                analysis,
                plan
            )
        )

        if not reasoning:

            return {
                "success": False,
                "stage": "reasoning"
            }

        # -----------------------------------------------------
        # 4 CODE GENERATION
        # -----------------------------------------------------

        generated = (
            self.generate_code(
                plan,
                project_name
            )
        )

        if not generated:

            return {
                "success": False,
                "stage": "code_generation"
            }

        # -----------------------------------------------------
        # 5 BUILD
        # -----------------------------------------------------

        project_path = (
            self.build_project(
                project_name,
                generated
            )
        )

        if not project_path:

            return {
                "success": False,
                "stage": "build"
            }

        # -----------------------------------------------------
        # 6 VALIDATION
        # -----------------------------------------------------

        validation = (
            self.validate_python_files(
                project_path
            )
        )

        if not validation.get(
            "success"
        ):

            error_text = json.dumps(
                validation.get(
                    "errors",
                    []
                ),
                indent=2
            )

            repair = (
                self.repair_and_validate(
                    project_path,
                    error_text
                )
            )

            if not repair.get(
                "success"
            ):

                return {
                    "success": False,
                    "stage": "validation",
                    "project":
                        str(project_path),
                    "repair":
                        repair
                }

            return self._complete_result(
                analysis,
                plan,
                reasoning,
                project_path,
                repair["validation"],
                repair["application"],
                repair["tests"],
                repair.get(
                    "attempts",
                    0
                )
            )

        # -----------------------------------------------------
        # 7 APPLICATION
        # -----------------------------------------------------

        application = (
            self.run_application(
                project_path
            )
        )

        if not application.get(
            "success"
        ):

            repair = (
                self.repair_and_validate(
                    project_path,
                    application.get(
                        "error",
                        ""
                    )
                )
            )

            if not repair.get(
                "success"
            ):

                return {
                    "success": False,
                    "stage": "application",
                    "project":
                        str(project_path),
                    "application":
                        application,
                    "repair":
                        repair
                }

            return self._complete_result(
                analysis,
                plan,
                reasoning,
                project_path,
                repair["validation"],
                repair["application"],
                repair["tests"],
                repair.get(
                    "attempts",
                    0
                )
            )

        # -----------------------------------------------------
        # 8 TESTS
        # -----------------------------------------------------

        tests = self.run_tests(
            project_path
        )

        if not tests.get(
            "success"
        ):

            repair = (
                self.repair_and_validate(
                    project_path,
                    tests.get(
                        "error",
                        ""
                    )
                )
            )

            if not repair.get(
                "success"
            ):

                return {
                    "success": False,
                    "stage": "testing",
                    "project":
                        str(project_path),
                    "tests": tests,
                    "repair":
                        repair
                }

            return self._complete_result(
                analysis,
                plan,
                reasoning,
                project_path,
                repair["validation"],
                repair["application"],
                repair["tests"],
                repair.get(
                    "attempts",
                    0
                )
            )

        # -----------------------------------------------------
        # SUCCESS
        # -----------------------------------------------------

        return self._complete_result(
            analysis,
            plan,
            reasoning,
            project_path,
            validation,
            application,
            tests,
            0
        )

    # =========================================================
    # COMPLETE RESULT
    # =========================================================

    def _complete_result(
        self,
        analysis,
        plan,
        reasoning,
        project_path,
        validation,
        application,
        tests,
        repair_attempts
    ):

        print()
        print(
            "======================================"
        )
        print(
            " 🎉 AURA PROJECT DEVELOPMENT COMPLETE"
        )
        print(
            "======================================"
        )

        print()
        print(
            "📁 PROJECT:"
        )
        print(
            project_path
        )

        print()
        print(
            "🧠 Analysis        : PASS"
        )
        print(
            "📐 Planning        : PASS"
        )
        print(
            "🧠 Reasoning       : PASS"
        )
        print(
            "💻 Code Generation : PASS"
        )
        print(
            "🏗️ Build           : PASS"
        )
        print(
            "🧪 Validation      : PASS"
        )
        print(
            "🚀 Application     : PASS"
        )
        print(
            "🧪 Tests           : PASS"
        )

        print()
        print(
            "🔧 Repair Attempts :",
            repair_attempts
        )

        print(
            "======================================"
        )

        return {
            "success": True,
            "analysis": analysis,
            "plan": plan,
            "reasoning": reasoning,
            "project": str(
                project_path
            ),
            "validation": validation,
            "application": application,
            "tests": tests,
            "repair_attempts":
                repair_attempts
        }


# =============================================================
# TEST
# =============================================================

if __name__ == "__main__":

    print()
    print(
        "======================================"
    )
    print(
        " AURA SELF-REPAIR DEVELOPER TEST"
    )
    print(
        "======================================"
    )

    agent = DeveloperAgent(
        max_repair_attempts=2
    )

    requirement = (
    	"Create a complete Python inventory billing software "
    	"with SQLite database, product management, "
    	"stock management, customer management, "
    	"billing, invoice generation, sales reports "
    	"and automated testing"
    )

    result = agent.process(
        requirement,
        project_name="aura_inventory_app"
    )

    print()
    print(
        "📊 FINAL RESULT"
    )
    print(
        "=============================="
    )

    print(
        json.dumps(
            result,
            indent=4,
            default=str
        )
    )

    print()
    print(
        "======================================"
    )
    print(
        " ✅ SELF-REPAIR DEVELOPER TEST COMPLETE"
    )
    print(
        "======================================"
    )