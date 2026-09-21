class CodeGenerator:

    def __init__(self, provider):

        self.provider = provider

    def generate(
        self,
        task,
        requirements,
        architecture
    ):

        return self.provider.generate_code(
            task=task,
            requirements=requirements,
            architecture=architecture
        )

    def fix(
        self,
        task,
        requirements,
        architecture,
        files,
        errors
    ):

        return self.provider.fix_code(
            task=task,
            requirements=requirements,
            architecture=architecture,
            files=files,
            errors=errors
        )