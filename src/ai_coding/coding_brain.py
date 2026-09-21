import os

from .config import CodingConfig

from .providers import (
    MockProvider,
    OpenAIProvider,
    GeminiProvider
)
from .analysis import RequirementAnalyzer
from .architecture import Architect
from .generation import CodeGenerator
from .project import ProjectBuilder
from .execution import Sandbox
from .testing import TestEngine
from .debugging import Debugger


class CodingBrain:

    def __init__(
        self,
        workspace="workspace",
        provider=None
    ):

        self.config = CodingConfig(
            workspace=workspace
        )

        if provider is not None:

            self.provider = provider

        else:

            use_real_ai = os.getenv(
                "AURA_USE_REAL_AI",
                "false"
            ).lower() == "true"

            if use_real_ai:

                self.provider = GeminiProvider()

            else:

                self.provider = MockProvider()

        self.analyzer = RequirementAnalyzer()

        self.architect = Architect()

        self.generator = CodeGenerator(
            self.provider
        )

        self.builder = ProjectBuilder(
            self.config.workspace
        )

        self.sandbox = Sandbox(
            timeout=self.config.timeout
        )

        self.testing = TestEngine(
            self.sandbox
        )

        self.debugger = Debugger()

    def develop(self, request):

        requirements = self.analyzer.analyze(
            request
        )

        architecture = self.architect.design(
            requirements
        )

        result = self.generator.generate(
            request,
            requirements,
            architecture
        )

        return result