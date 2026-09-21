import re


class RequirementAnalyzer:

    def __init__(self):
        print("🧠 Requirement Analyzer: READY")

    # =========================================================
    # ANALYZE USER REQUIREMENT
    # =========================================================

    def analyze(self, requirement):

        if not requirement or not requirement.strip():

            return {
                "success": False,
                "message": "No requirement provided."
            }

        text = requirement.strip()
        lower = text.lower()

        project_type = self.detect_project_type(lower)
        technology = self.detect_technology(lower)
        features = self.detect_features(lower)

        return {
            "success": True,
            "original_requirement": text,
            "project_type": project_type,
            "technology": technology,
            "features": features
        }

    # =========================================================
    # PROJECT TYPE
    # =========================================================

    def detect_project_type(self, text):

        if any(
            word in text
            for word in [
                "website",
                "web app",
                "web application",
                "flask",
                "django"
            ]
        ):
            return "web_application"

        if any(
            word in text
            for word in [
                "desktop app",
                "desktop application",
                "tkinter",
                "desktop software"
            ]
        ):
            return "desktop_application"

        if any(
            word in text
            for word in [
                "api",
                "rest api",
                "backend api"
            ]
        ):
            return "api"

        if any(
            word in text
            for word in [
                "mobile app",
                "android app",
                "ios app"
            ]
        ):
            return "mobile_application"

        if any(
            word in text
            for word in [
                "data analysis",
                "data analyst",
                "analytics"
            ]
        ):
            return "data_analysis"

        if any(
            word in text
            for word in [
                "ai",
                "artificial intelligence",
                "machine learning",
                "ml model"
            ]
        ):
            return "ai_application"

        if any(
            word in text
            for word in [
                "calculator",
                "billing",
                "inventory",
                "software",
                "application",
                "app"
            ]
        ):
            return "software_application"

        return "python_project"

    # =========================================================
    # TECHNOLOGY
    # =========================================================

    def detect_technology(self, text):

        technologies = []

        technology_map = {

            "python": [
                "python",
                "py"
            ],

            "flask": [
                "flask"
            ],

            "django": [
                "django"
            ],

            "tkinter": [
                "tkinter"
            ],

            "sqlite": [
                "sqlite",
                "sqlite3"
            ],

            "mysql": [
                "mysql"
            ],

            "postgresql": [
                "postgresql",
                "postgres"
            ],

            "javascript": [
                "javascript",
                "js"
            ],

            "react": [
                "react",
                "reactjs"
            ],

            "html_css": [
                "html",
                "css"
            ],

            "power_bi": [
                "power bi"
            ],

            "pandas": [
                "pandas"
            ],

            "machine_learning": [
                "machine learning",
                "ml"
            ]
        }

        for technology, keywords in technology_map.items():

            if any(
                keyword in text
                for keyword in keywords
            ):

                technologies.append(
                    technology
                )

        if not technologies:

            technologies.append("python")

        return technologies

    # =========================================================
    # FEATURES
    # =========================================================

    def detect_features(self, text):

        features = []

        feature_map = {

            "authentication": [
                "login",
                "authentication",
                "signup",
                "sign up",
                "register"
            ],

            "database": [
                "database",
                "db",
                "sqlite",
                "mysql",
                "postgres"
            ],

            "billing": [
                "billing",
                "invoice",
                "bill"
            ],

            "inventory": [
                "inventory",
                "stock",
                "products"
            ],

            "dashboard": [
                "dashboard",
                "admin panel",
                "admin dashboard"
            ],

            "search": [
                "search",
                "filter"
            ],

            "reports": [
                "report",
                "reports",
                "analytics"
            ],

            "api": [
                "api",
                "rest api"
            ],

            "voice": [
                "voice",
                "speech",
                "voice command"
            ],

            "ai": [
                "ai",
                "artificial intelligence",
                "assistant",
                "chatbot"
            ],

            "payment": [
                "payment",
                "razorpay",
                "stripe",
                "upi"
            ],

            "export": [
                "export",
                "excel",
                "csv",
                "pdf"
            ],

            "testing": [
                "test",
                "testing",
                "pytest"
            ]
        }

        for feature, keywords in feature_map.items():

            if any(
                keyword in text
                for keyword in keywords
            ):

                features.append(
                    feature
                )

        return features

    # =========================================================
    # HUMAN READABLE SUMMARY
    # =========================================================

    def summary(self, analysis):

        if not analysis.get("success"):
            return analysis.get(
                "message",
                "Analysis failed."
            )

        project_type = analysis[
            "project_type"
        ]

        technologies = ", ".join(
            analysis["technology"]
        )

        features = analysis["features"]

        if features:

            feature_text = ", ".join(
                features
            )

        else:

            feature_text = "basic functionality"

        return (
            f"Project Type: {project_type}\n"
            f"Technology: {technologies}\n"
            f"Features: {feature_text}"
        )


# =============================================================
# TEST
# =============================================================

if __name__ == "__main__":

    print()
    print("======================================")
    print(" AURA REQUIREMENT ANALYZER TEST")
    print("======================================")
    print()

    analyzer = RequirementAnalyzer()

    test_requirements = [

        "Create a Python inventory billing application",

        "Build a Flask website with login and database",

        "Create a desktop application using Tkinter",

        "Build an AI chatbot with voice commands",

        "Create a data analysis project using Python and pandas"
    ]

    for requirement in test_requirements:

        print()
        print("👤 REQUIREMENT:")
        print(requirement)

        result = analyzer.analyze(
            requirement
        )

        print()
        print("🧠 AURA ANALYSIS:")

        print(
            analyzer.summary(result)
        )

        print()
        print("--------------------------------------")

    print()
    print("======================================")
    print(" ✅ REQUIREMENT ANALYZER TEST COMPLETE")
    print("======================================")
