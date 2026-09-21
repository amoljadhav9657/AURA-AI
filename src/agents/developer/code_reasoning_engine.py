from pathlib import Path


class CodeReasoningEngine:

    def __init__(self):
        print("🧠 Code Reasoning Engine: READY")

    # =========================================================
    # REASON ABOUT PROJECT
    # =========================================================

    def reason(self, analysis, plan):

        if not analysis:
            return {
                "success": False,
                "error": "Analysis is missing."
            }

        if not plan:
            return {
                "success": False,
                "error": "Project plan is missing."
            }

        project_type = analysis.get(
            "project_type",
            "software_application"
        )

        technologies = analysis.get(
            "technology",
            analysis.get(
                "technologies",
                ["python"]
            )
        )

        features = analysis.get(
            "features",
            []
        )

        files = plan.get(
            "files",
            []
        )

        dependencies = plan.get(
            "dependencies",
            []
        )

        architecture = self._select_architecture(
            project_type,
            technologies,
            features
        )

        layers = self._create_layers(
            features
        )

        implementation_order = self._create_implementation_order(
            files,
            features
        )

        testing_strategy = self._create_testing_strategy(
            features
        )

        reasoning = {
            "success": True,
            "project_type": project_type,
            "technologies": technologies,
            "features": features,
            "architecture": architecture,
            "layers": layers,
            "files": files,
            "dependencies": dependencies,
            "implementation_order": implementation_order,
            "testing_strategy": testing_strategy
        }

        return reasoning

    # =========================================================
    # ARCHITECTURE
    # =========================================================

    def _select_architecture(
        self,
        project_type,
        technologies,
        features
    ):

        technology_text = " ".join(
            str(item).lower()
            for item in technologies
        )

        feature_text = " ".join(
            str(item).lower()
            for item in features
        )

        if (
            "flask" in technology_text
            or project_type == "web_application"
        ):

            return {
                "style": "layered_web_architecture",
                "layers": [
                    "routes",
                    "business_logic",
                    "database",
                    "templates"
                ]
            }

        if project_type == "desktop_application":

            return {
                "style": "desktop_layered_architecture",
                "layers": [
                    "ui",
                    "business_logic",
                    "data"
                ]
            }

        if project_type == "ai_application":

            return {
                "style": "ai_agent_architecture",
                "layers": [
                    "input",
                    "reasoning",
                    "tools",
                    "memory",
                    "output"
                ]
            }

        if project_type == "data_analysis":

            return {
                "style": "data_analysis_pipeline",
                "layers": [
                    "input",
                    "cleaning",
                    "analysis",
                    "visualization",
                    "reporting"
                ]
            }

        if (
            "database" in feature_text
            and "billing" in feature_text
            and "inventory" in feature_text
        ):

            return {
                "style": "business_application_architecture",
                "layers": [
                    "application",
                    "billing",
                    "inventory",
                    "database",
                    "reports"
                ]
            }

        return {
            "style": "modular_python_application",
            "layers": [
                "application",
                "business_logic",
                "utilities"
            ]
        }

    # =========================================================
    # PROJECT LAYERS
    # =========================================================

    def _create_layers(self, features):

        feature_text = " ".join(
            str(item).lower()
            for item in features
        )

        layers = []

        layers.append(
            "core_application"
        )

        if "database" in feature_text:
            layers.append(
                "database_layer"
            )

        if "inventory" in feature_text:
            layers.append(
                "inventory_layer"
            )

        if "billing" in feature_text:
            layers.append(
                "billing_layer"
            )

        if "authentication" in feature_text:
            layers.append(
                "authentication_layer"
            )

        if "reports" in feature_text:
            layers.append(
                "reporting_layer"
            )

        if "voice" in feature_text:
            layers.append(
                "voice_layer"
            )

        if "ai" in feature_text:
            layers.append(
                "ai_reasoning_layer"
            )

        return layers

    # =========================================================
    # IMPLEMENTATION ORDER
    # =========================================================

    def _create_implementation_order(
        self,
        files,
        features
    ):

        ordered_files = []

        priority_keywords = [
            "config",
            "database",
            "models",
            "utils",
            "auth",
            "inventory",
            "stock",
            "billing",
            "invoice",
            "reports",
            "ai_engine",
            "voice",
            "main",
            "tests"
        ]

        for keyword in priority_keywords:

            for file_name in files:

                file_text = str(
                    file_name
                ).lower()

                if keyword in file_text:

                    if file_name not in ordered_files:

                        ordered_files.append(
                            file_name
                        )

        for file_name in files:

            if file_name not in ordered_files:

                ordered_files.append(
                    file_name
                )

        return ordered_files

    # =========================================================
    # TESTING STRATEGY
    # =========================================================

    def _create_testing_strategy(
        self,
        features
    ):

        feature_text = " ".join(
            str(item).lower()
            for item in features
        )

        tests = [
            "syntax_validation",
            "application_startup"
        ]

        if "database" in feature_text:
            tests.append(
                "database_operations"
            )

        if "inventory" in feature_text:
            tests.append(
                "inventory_operations"
            )

        if "billing" in feature_text:
            tests.append(
                "billing_operations"
            )

        if "authentication" in feature_text:
            tests.append(
                "authentication"
            )

        if "reports" in feature_text:
            tests.append(
                "report_generation"
            )

        tests.append(
            "automated_regression_tests"
        )

        return tests

    # =========================================================
    # DISPLAY REASONING
    # =========================================================

    def display_reasoning(
        self,
        reasoning
    ):

        print()
        print(
            "🧠 CODE REASONING"
        )
        print(
            "=============================="
        )

        print(
            "Architecture:",
            reasoning.get(
                "architecture",
                {}
            ).get(
                "style",
                "unknown"
            )
        )

        print()
        print("📚 LAYERS")

        for layer in reasoning.get(
            "layers",
            []
        ):

            print(
                "   └──",
                layer
            )

        print()
        print(
            "💻 IMPLEMENTATION ORDER"
        )

        for index, file_name in enumerate(
            reasoning.get(
                "implementation_order",
                []
            ),
            start=1
        ):

            print(
                f"   {index}. {file_name}"
            )

        print()
        print(
            "🧪 TESTING STRATEGY"
        )

        for test in reasoning.get(
            "testing_strategy",
            []
        ):

            print(
                "   └──",
                test
            )


# =============================================================
# TEST
# =============================================================

if __name__ == "__main__":

    print()
    print(
        "======================================"
    )
    print(
        " AURA CODE REASONING ENGINE TEST"
    )
    print(
        "======================================"
    )

    engine = CodeReasoningEngine()

    analysis = {
        "success": True,
        "project_type": "software_application",
        "technology": [
            "python"
        ],
        "features": [
            "database",
            "billing",
            "inventory",
            "reports",
            "testing"
        ]
    }

    plan = {
        "success": True,
        "files": [
            "main.py",
            "database.py",
            "models.py",
            "billing.py",
            "invoice.py",
            "inventory.py",
            "stock.py",
            "reports.py",
            "tests/test_main.py"
        ],
        "dependencies": [
            "pytest"
        ]
    }

    reasoning = engine.reason(
        analysis,
        plan
    )

    if reasoning.get("success"):

        engine.display_reasoning(
            reasoning
        )

        print()
        print(
            "======================================"
        )
        print(
            " ✅ CODE REASONING TEST COMPLETE"
        )
        print(
            "======================================"
        )

    else:

        print()
        print(
            "❌ CODE REASONING FAILED"
        )

        print(
            reasoning
        )