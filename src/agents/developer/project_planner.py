from pathlib import Path


class ProjectPlanner:

    def __init__(self):
        print("📐 Project Planner: READY")

    # =========================================================
    # CREATE PROJECT PLAN
    # =========================================================

    def create_plan(self, analysis):

        if not analysis:
            return {
                "success": False,
                "message": "No analysis provided."
            }

        if not analysis.get("success"):
            return {
                "success": False,
                "message": "Requirement analysis failed."
            }

        project_type = analysis.get(
            "project_type",
            "python_project"
        )

        technologies = analysis.get(
            "technology",
            ["python"]
        )

        features = analysis.get(
            "features",
            []
        )

        files = self.plan_files(
            project_type,
            technologies,
            features
        )

        dependencies = self.plan_dependencies(
            project_type,
            technologies,
            features
        )

        steps = self.plan_steps(
            project_type,
            technologies,
            features
        )

        return {
            "success": True,
            "project_type": project_type,
            "technologies": technologies,
            "features": features,
            "files": files,
            "dependencies": dependencies,
            "steps": steps
        }

    # =========================================================
    # PLAN FILES
    # =========================================================

    def plan_files(
        self,
        project_type,
        technologies,
        features
    ):

        files = [
            "main.py",
            "README.md"
        ]

        # -----------------------------------------------------
        # DATABASE
        # -----------------------------------------------------

        if "database" in features:

            files.extend([
                "database.py",
                "models.py"
            ])

        # -----------------------------------------------------
        # AUTHENTICATION
        # -----------------------------------------------------

        if "authentication" in features:

            files.extend([
                "auth.py"
            ])

        # -----------------------------------------------------
        # BILLING
        # -----------------------------------------------------

        if "billing" in features:

            files.extend([
                "billing.py",
                "invoice.py"
            ])

        # -----------------------------------------------------
        # INVENTORY
        # -----------------------------------------------------

        if "inventory" in features:

            files.extend([
                "inventory.py",
                "stock.py"
            ])

        # -----------------------------------------------------
        # DASHBOARD
        # -----------------------------------------------------

        if "dashboard" in features:

            files.extend([
                "dashboard.py"
            ])

        # -----------------------------------------------------
        # REPORTS
        # -----------------------------------------------------

        if "reports" in features:

            files.extend([
                "reports.py"
            ])

        # -----------------------------------------------------
        # API
        # -----------------------------------------------------

        if "api" in features:

            files.extend([
                "api.py"
            ])

        # -----------------------------------------------------
        # VOICE
        # -----------------------------------------------------

        if "voice" in features:

            files.extend([
                "voice.py"
            ])

        # -----------------------------------------------------
        # AI
        # -----------------------------------------------------

        if "ai" in features:

            files.extend([
                "ai_engine.py"
            ])

        # -----------------------------------------------------
        # PAYMENT
        # -----------------------------------------------------

        if "payment" in features:

            files.extend([
                "payment.py"
            ])

        # -----------------------------------------------------
        # EXPORT
        # -----------------------------------------------------

        if "export" in features:

            files.extend([
                "export.py"
            ])

        # -----------------------------------------------------
        # TESTS
        # -----------------------------------------------------

        files.append(
            "tests/test_main.py"
        )

        return files

    # =========================================================
    # PLAN DEPENDENCIES
    # =========================================================

    def plan_dependencies(
        self,
        project_type,
        technologies,
        features
    ):

        dependencies = []

        dependency_map = {

            "flask": "Flask",

            "django": "Django",

            "pandas": "pandas",

            "power_bi": "powerbi",

            "machine_learning": "scikit-learn",

            "tkinter": "tkinter",

            "sqlite": "sqlite3"
        }

        for technology in technologies:

            dependency = dependency_map.get(
                technology
            )

            if dependency and dependency not in dependencies:

                dependencies.append(
                    dependency
                )

        if "testing" in features:

            dependencies.append(
                "pytest"
            )

        return dependencies

    # =========================================================
    # DEVELOPMENT STEPS
    # =========================================================

    def plan_steps(
        self,
        project_type,
        technologies,
        features
    ):

        steps = [
            "Create project structure",
            "Create configuration",
            "Implement core application",
        ]

        if "database" in features:

            steps.append(
                "Implement database layer"
            )

        if "authentication" in features:

            steps.append(
                "Implement authentication"
            )

        if "inventory" in features:

            steps.append(
                "Implement inventory management"
            )

        if "billing" in features:

            steps.append(
                "Implement billing system"
            )

        if "dashboard" in features:

            steps.append(
                "Implement dashboard"
            )

        if "reports" in features:

            steps.append(
                "Implement reports"
            )

        if "api" in features:

            steps.append(
                "Implement API endpoints"
            )

        if "voice" in features:

            steps.append(
                "Implement voice interface"
            )

        if "ai" in features:

            steps.append(
                "Implement AI engine"
            )

        if "payment" in features:

            steps.append(
                "Implement payment integration"
            )

        if "export" in features:

            steps.append(
                "Implement export functionality"
            )

        steps.extend([
            "Create documentation",
            "Run validation",
            "Run automated tests"
        ])

        return steps

    # =========================================================
    # DISPLAY PLAN
    # =========================================================

    def display_plan(self, plan):

        if not plan.get("success"):

            print(
                "❌",
                plan.get(
                    "message",
                    "Planning failed."
                )
            )

            return

        print()
        print("📐 PROJECT PLAN")
        print("==============================")

        print()
        print(
            "Project Type:",
            plan["project_type"]
        )

        print(
            "Technology:",
            ", ".join(
                plan["technologies"]
            )
        )

        print(
            "Features:",
            ", ".join(
                plan["features"]
            )
            if plan["features"]
            else "basic"
        )

        print()
        print("📁 FILE STRUCTURE")

        for file in plan["files"]:

            print(
                "   └──",
                file
            )

        print()
        print("📦 DEPENDENCIES")

        if plan["dependencies"]:

            for dependency in plan["dependencies"]:

                print(
                    "   └──",
                    dependency
                )

        else:

            print(
                "   └── No external dependencies"
            )

        print()
        print("🚀 DEVELOPMENT STEPS")

        for index, step in enumerate(
            plan["steps"],
            start=1
        ):

            print(
                f"   {index}. {step}"
            )


# =============================================================
# TEST
# =============================================================

if __name__ == "__main__":

    print()
    print("======================================")
    print(" AURA PROJECT PLANNER TEST")
    print("======================================")
    print()

    # Import our Requirement Analyzer

    from .requirement_analyzer import (
    	RequirementAnalyzer
    )

    analyzer = RequirementAnalyzer()

    planner = ProjectPlanner()

    requirements = [

        "Create a Python inventory billing application",

        "Build a Flask website with login and database",

        "Build an AI chatbot with voice commands"
    ]

    for requirement in requirements:

        print()
        print("👤 REQUIREMENT:")
        print(requirement)

        analysis = analyzer.analyze(
            requirement
        )

        plan = planner.create_plan(
            analysis
        )

        planner.display_plan(
            plan
        )

        print()
        print("--------------------------------------")

    print()
    print("======================================")
    print(" ✅ PROJECT PLANNER TEST COMPLETE")
    print("======================================")
