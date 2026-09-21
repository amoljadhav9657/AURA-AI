class DevelopmentLoop:

    def __init__(
        self,
        generator,
        builder,
        test_engine,
        debugger,
        max_iterations=3
    ):
        self.generator = generator
        self.builder = builder
        self.test_engine = test_engine
        self.debugger = debugger
        self.max_iterations = max_iterations

    # --------------------------------------------------
    # MERGE AI FIXES
    # --------------------------------------------------

    def _merge_files(
        self,
        current_files,
        fixed_files
    ):

        merged = dict(current_files)

        for path, content in fixed_files.items():

            merged[path] = content

        return merged

    # --------------------------------------------------
    # DEVELOPMENT LOOP
    # --------------------------------------------------

    def execute(
        self,
        task,
        requirements,
        architecture,
        project_path
    ):

        history = []

        # ---------------------------------------------
        # INITIAL CODE GENERATION
        # ---------------------------------------------

        files = self.generator.generate(
            task=task,
            requirements=requirements,
            architecture=architecture
        )

        created = self.builder.build(
            project_path,
            files
        )

        # ---------------------------------------------
        # AUTONOMOUS DEVELOPMENT LOOP
        # ---------------------------------------------

        for iteration in range(
            1,
            self.max_iterations + 1
        ):

            validation = self.test_engine.validate(
                project_path
            )

            debug = self.debugger.analyze(
                validation
            )

            history.append({
                "iteration": iteration,
                "files": list(files.keys()),
                "created": created,
                "validation": validation,
                "debug": debug
            })

            # -----------------------------------------
            # SUCCESS
            # -----------------------------------------

            if validation["overall_passed"]:

                return {
                    "status": "success",
                    "iterations": iteration,
                    "history": history
                }

            # -----------------------------------------
            # MAX ITERATIONS
            # -----------------------------------------

            if iteration >= self.max_iterations:

                break

            # -----------------------------------------
            # BUILD FIX REQUEST
            # -----------------------------------------

            fix_request = (
                self.debugger.build_fix_request(
                    debug["errors"]
                )
            )

            if not fix_request:

                break

            # -----------------------------------------
            # AI REPAIR
            # -----------------------------------------

            fixed_files = self.generator.fix(
                task=task,
                requirements=requirements,
                architecture=architecture,
                files=files,
                errors=fix_request
            )

            # -----------------------------------------
            # IMPORTANT:
            # MERGE AI REPAIR WITH EXISTING PROJECT
            # -----------------------------------------

            files = self._merge_files(
                files,
                fixed_files
            )

            # -----------------------------------------
            # REBUILD PROJECT
            # -----------------------------------------

            created = self.builder.build(
                project_path,
                files
            )

        # ---------------------------------------------
        # FAILED
        # ---------------------------------------------

        return {
            "status": "failed",
            "iterations": len(history),
            "history": history
        }