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

    # ==================================================
    # STRUCTURE VALIDATION
    # ==================================================

    def _structure_errors(
        self,
        files,
        requirements,
        architecture
    ):

        result = self.generator.validate_generated_structure(
            files=files,
            requirements=requirements,
            architecture=architecture
        )

        return result["errors"]

    # ==================================================
    # DEVELOPMENT LOOP
    # ==================================================

    def execute(
        self,
        task,
        requirements,
        architecture,
        project_path
    ):

        history = []

        # ==================================================
        # INITIAL AI GENERATION
        # ==================================================

        files = self.generator.generate(
            task=task,
            requirements=requirements,
            architecture=architecture
        )

        created = self.builder.build(
            project_path,
            files
        )

        # ==================================================
        # AUTONOMOUS DEVELOPMENT
        # ==================================================

        for iteration in range(
            1,
            self.max_iterations + 1
        ):

            # --------------------------------------------------
            # STRUCTURE CHECK
            # --------------------------------------------------

            structure_errors = self._structure_errors(
                files=files,
                requirements=requirements,
                architecture=architecture
            )

            # --------------------------------------------------
            # CODE / TEST VALIDATION
            # --------------------------------------------------

            validation = self.test_engine.validate(
                project_path
            )

            # --------------------------------------------------
            # DEBUGGER
            # --------------------------------------------------

            debug = self.debugger.analyze(
                validation
            )

            # --------------------------------------------------
            # COMBINE STRUCTURE ERRORS + TEST ERRORS
            # --------------------------------------------------

            all_errors = []

            all_errors.extend(
                structure_errors
            )

            all_errors.extend(
                debug.get("errors", [])
            )

            overall_passed = (
                validation["overall_passed"]
                and not structure_errors
            )

            history.append({

                "iteration": iteration,

                "files": list(files.keys()),

                "created": created,

                "structure_errors": structure_errors,

                "validation": validation,

                "debug": debug,

                "overall_passed": overall_passed
            })

            # ==================================================
            # SUCCESS
            # ==================================================

            if overall_passed:

                return {
                    "status": "success",
                    "iterations": iteration,
                    "history": history
                }

            # ==================================================
            # MAX ITERATIONS
            # ==================================================

            if iteration >= self.max_iterations:

                break

            # ==================================================
            # BUILD AI FIX REQUEST
            # ==================================================

            fix_errors = list(all_errors)

            if not fix_errors:

                break

            fix_request = {

                "instruction": (
                    "Repair the generated project completely. "
                    "Preserve working functionality. "
                    "Do not remove or weaken existing tests. "
                    "Add every missing required file and "
                    "functional test. "
                    "Return complete changed files."
                ),

                "errors": fix_errors
            }

            # ==================================================
            # AI REPAIR
            # ==================================================

            fixed_files = self.generator.fix(
                task=task,
                requirements=requirements,
                architecture=architecture,
                files=files,
                errors=fix_request
            )

            # ==================================================
            # REBUILD PROJECT
            # ==================================================

            files = fixed_files

            created = self.builder.build(
                project_path,
                files
            )

        # ==================================================
        # FAILED
        # ==================================================

        return {
            "status": "failed",
            "iterations": len(history),
            "history": history
        }