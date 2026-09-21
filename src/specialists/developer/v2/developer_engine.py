import os

from src.ai_coding.providers import (
    MockProvider,
    OpenAIProvider,
    GeminiProvider
)
from .task_analyzer import TaskAnalyzerV2
from .architect import Architect
from .ai_codegen import AICodeGenerator
from .project_builder import ProjectBuilder
from .sandbox import Sandbox
from .test_engine import TestEngine
from .debugger import Debugger
from .development_loop import DevelopmentLoop


class DeveloperEngineV2:

    def __init__(
        self,
        workspace="workspace",
        provider=None
    ):

        if provider is None:

            use_real_ai = os.getenv(
                "AURA_USE_REAL_AI",
                "false"
            ).lower() == "true"

            if use_real_ai:
                provider = GeminiProvider()
            else:
                provider = MockProvider()

        self.analyzer = TaskAnalyzerV2()

        self.architect = Architect()

        self.generator = AICodeGenerator(
            provider=provider
        )

        self.builder = ProjectBuilder(
            workspace=workspace
        )

        self.sandbox = Sandbox()

        self.test_engine = TestEngine(
            self.sandbox
        )

        self.debugger = Debugger()

        self.loop = DevelopmentLoop(
            generator=self.generator,
            builder=self.builder,
            test_engine=self.test_engine,
            debugger=self.debugger,
            max_iterations=3
        )        

    def develop(
        self,
        task,
        project_name="aura_v2_project"
    ):

        analysis = self.analyzer.analyze(
            task
        )

        architecture = self.architect.design(
            analysis
        )

        project_path = (
            self.builder.create_project(
                project_name
            )
        )

        result = self.loop.execute(
    	    task=task,
    	    requirements=analysis,
   	    architecture=architecture,
    	    project_path=project_path
	)

        return {
            "task": task,
            "analysis": analysis,
            "architecture": architecture,
            "project_path": str(
                project_path.resolve()
            ),
            "result": result
        }
