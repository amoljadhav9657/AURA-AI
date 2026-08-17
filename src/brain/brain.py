from src.task.task_manager import TaskManager
from .intent_classifier import IntentClassifier
from .decision_engine import DecisionEngine
from src.memory.memory_manager import MemoryManager
from src.system.system_manager import SystemManager
from src.context.context_engine import ContextEngine
from src.action.action_executor import ActionExecutor


class Brain:

    def __init__(self):
        self.intent = IntentClassifier()
        self.engine = DecisionEngine()
        self.memory = MemoryManager()
        self.system = SystemManager()
        self.action = ActionExecutor()
        self.task = TaskManager()
        self.context = ContextEngine(self.memory)

    def process(self, text):

        text = text.strip()

        if not text:
            return "Please say something."

        self.memory.remember_conversation("user", text)
        # System commands
        result = self.system.execute(text)

                # Detect intent
        intent = self.intent.detect(text)

        # ---------------------------------------------------------
        # v0.27.0 - Task Intelligence Routing
        # ---------------------------------------------------------
                # ---------------------------------------------------------
        # v0.27.0 - Task Lifecycle
        # ---------------------------------------------------------

        if intent == "task_status":

            status = self.task.get_status()

            executor = status["executor"]
            current_task = executor["task"]
            task_status = executor["status"]

            if current_task:

                response = (
                    f"Current task: {current_task}. "
                    f"Status: {task_status}."
                )

            else:

                response = "There is no active task."

            self.memory.remember_conversation(
                "aura",
                response
            )

            return response

        if intent == "task_complete":

            result = self.task.complete_current()

            if result.get("status") == "completed":

                response = (
                    f"Task completed: {result['task']}"
                )

            else:

                response = result.get(
                    "message",
                    "There is no active task."
                )

            self.memory.remember_conversation(
                "aura",
                response
            )

            return response
                    # ---------------------------------------------------------
        # v0.28.0 - Natural Task Control
        # ---------------------------------------------------------

        if intent == "task_status":

            status = self.task.get_status()

            executor = status["executor"]
            current_task = executor["task"]
            task_status = executor["status"]

            if current_task:
                response = (
                    f"Current task: {current_task}. "
                    f"Status: {task_status}."
                )
            else:
                response = "I don't have an active task."

            self.memory.remember_conversation(
                "aura",
                response
            )

            return response

        if intent == "task_progress":

            progress = self.task.get_progress()

            response = (
                f"Task progress: "
                f"{progress['completed']}/{progress['total']} "
                f"completed "
                f"({progress['progress']:.1f}%)."
            )

            self.memory.remember_conversation(
                "aura",
                response
            )

            return response

        if intent == "subtask_start":

            try:
                subtask_id = int(
                    text.split()[-1]
                )
            except ValueError:
                response = "Please provide a valid subtask number."

                self.memory.remember_conversation(
                    "aura",
                    response
                )

                return response

            result = self.task.start_subtask(subtask_id)

            if result.get("status") == "error":
                response = result["message"]
            else:
                response = (
                    f"Subtask {result['id']} started: "
                    f"{result['task']}"
                )

            self.memory.remember_conversation(
                "aura",
                response
            )

            return response

        if intent == "subtask_complete":

            try:
                subtask_id = int(
                    text.split()[-1]
                )
            except ValueError:
                response = "Please provide a valid subtask number."

                self.memory.remember_conversation(
                    "aura",
                    response
                )

                return response

            result = self.task.complete_subtask(subtask_id)

            if result.get("status") == "error":
                response = result["message"]
            else:
                response = (
                    f"Subtask {result['id']} completed: "
                    f"{result['task']}"
                )

            self.memory.remember_conversation(
                "aura",
                response
            )

            return response

        if intent == "subtask_fail":

            try:
                parts = text.split()
                subtask_id = int(parts[2])
                reason = " ".join(parts[3:]).strip()

            except (ValueError, IndexError):
                response = (
                    "Use: fail subtask <number> <reason>"
                )

                self.memory.remember_conversation(
                    "aura",
                    response
                )

                return response

            result = self.task.fail_subtask(
                subtask_id,
                reason
            )

            if result.get("status") == "error":
                response = result["message"]
            else:
                response = (
                    f"Subtask {result['id']} failed: "
                    f"{result['task']}"
                )

            self.memory.remember_conversation(
                "aura",
                response
            )

            return response

        if intent == "task_complete":

            result = self.task.complete_current()

            if result.get("status") == "error":
                response = result["message"]
            else:
                response = (
                    f"Task completed: "
                    f"{result['task']}"
                )

            self.memory.remember_conversation(
                "aura",
                response
            )

            return response

        if intent == "task":

            result = self.task.create_and_start(text)

            if result.get("status") == "running":

                response = f"Task started: {result['task']}"

                self.memory.remember_conversation(
                    "aura",
                    response
                )

                return response

            response = result.get(
                "message",
                "Unable to start task."
            )

            self.memory.remember_conversation(
                "aura",
                response
            )

            return response

        # ---------------------------------------------------------
        # Existing v0.25.0 - Action Executor Routing
        # ---------------------------------------------------------

        # ---------------------------------------------------------
        # v0.25.0 - Action Executor Routing
        # ---------------------------------------------------------

        if intent == "system_action":

            command_type, value = self.system.parser.parse(text)

            # Application commands → ActionExecutor
            if command_type == "app":

                action_result = self.action.execute(
                    "open_app",
                    value
                )

                if action_result.get("status") == "completed":

                    response = action_result.get(
                        "result",
                        f"Completed: {value}"
                    )

                    self.memory.remember_conversation(
                        "aura",
                        response
                    )

                    return response

            # Other system commands remain on existing
            # SystemManager path for now.
            result = self.system.execute(text)

            if result:

                self.memory.remember_conversation(
                    "aura",
                    result
                )

                return result
        # Save user's name
        if intent == "memory_save_name":

            name = text[11:].strip()

            if name:
                self.memory.remember("name", name)

                response = f"Nice to meet you, {name}."
                self.memory.remember_conversation("aura", response)
                return response

            response = "Please tell me your name."
            self.memory.remember_conversation("aura", response)
            return response

        # Recall user's name
        if intent == "memory_recall_name":

            name = self.memory.recall("name")

            if name:
                response = f"Your name is {name}."
            else:
                response = "I don't know your name yet."

            self.memory.remember_conversation("aura", response)
            return response

        # Natural memory save
        if intent == "memory_save":

            statement = text[len("remember that "):].strip()

            if not statement:
                response = "What would you like me to remember?"
                self.memory.remember_conversation("aura", response)
                return response

            if " is " in statement:

                key, value = statement.split(" is ", 1)

                key = key.strip()
                value = value.strip()

                if key.startswith("my "):
                    key = key[3:].strip()

                if key and value:

                    self.memory.remember(key, value)

                    response = f"I'll remember that your {key} is {value}."
                    self.memory.remember_conversation("aura", response)
                    return response

            response = "I can remember facts in the form: remember that X is Y."
            self.memory.remember_conversation("aura", response)
            return response

        # Natural memory recall
        if intent == "memory_recall":

            key = text[len("what is my "):].strip().rstrip("?")

            if key:

                value = self.memory.recall(key)

                if value:
                    response = f"Your {key} is {value}."
                else:
                    response = f"I don't know your {key} yet."

                self.memory.remember_conversation("aura", response)
                return response

            response = "What would you like me to recall?"
            self.memory.remember_conversation("aura", response)
            return response
                # ---------------------------------------------------------
            # ---------------------------------------------------------
        # Basic Decision Engine
        # ---------------------------------------------------------

        if intent in ["greeting", "time", "date"]:

            response = self.engine.execute(intent)

            self.memory.remember_conversation(
                "aura",
                response
            )

            return response

        # ---------------------------------------------------------
        # Automatic Fact Memory
        # ---------------------------------------------------------

        if intent == "memory_auto_save":

            statement = text.strip()

            if statement.startswith("my "):
                statement = statement[3:].strip()

            if " is " in statement:

                key, value = statement.split(" is ", 1)

                key = key.strip()
                value = value.strip()

                if key and value:

                    self.memory.remember(key, value)

                    response = (
                        f"I'll remember that your {key} is {value}."
                    )

                    self.memory.remember_conversation(
                        "aura",
                        response
                    )

                    return response

            response = "I couldn't understand that fact."

            self.memory.remember_conversation(
                "aura",
                response
            )

            return response
                        # ---------------------------------------------------------
        # v0.20.0 - Context & Topic Router
        # ---------------------------------------------------------

        if intent == "unknown":

            lower_text = text.lower().strip()

            # =====================================================
            # 1. EXPLICIT TOPIC ROUTING
            # =====================================================

            if (
                lower_text.startswith("what about ")
                or lower_text.startswith("how about ")
            ):

                requested_topic = lower_text.split(" ", 2)[2]
                requested_topic = requested_topic.strip().rstrip("?!. ")

                topic = self.context.find_topic(requested_topic)

                if topic:

                    # IMPORTANT:
                    # Explicit topic ALWAYS replaces active topic.
                    self.context.set_active_topic(topic)

                    current_topic = topic["key"]
                    current_value = topic["value"]

                    response = (
                        f"We are still talking about your "
                        f"{current_topic}, {current_value}."
                    )

                    self.memory.remember_conversation(
                        "aura",
                        response
                    )

                    return response

            # =====================================================
            # 2. GENERIC FOLLOW-UP
            # =====================================================

            active_topic = self.context.get_active_topic()

            if active_topic and self.context.is_follow_up(text):

                current_topic = active_topic["key"]
                current_value = active_topic["value"]

                if "tell me more" in lower_text:

                    response = (
                        f"Your current topic is your "
                        f"{current_topic}, and you mentioned "
                        f"{current_value}."
                    )

                elif (
                    "like it" in lower_text
                    or "like this" in lower_text
                    or "like that" in lower_text
                ):

                    response = (
                        f"That's great! You really like "
                        f"{current_value}."
                    )

                elif "good" in lower_text:

                    response = (
                        f"Yes, {current_value} sounds good."
                    )

                elif "why" in lower_text:

                    response = (
                        f"We were talking about your "
                        f"{current_topic}, which is "
                        f"{current_value}."
                    )

                else:

                    response = (
                        f"We are still talking about your "
                        f"{current_topic}, {current_value}."
                    )

                self.memory.remember_conversation(
                    "aura",
                    response
                )

                return response

            # =====================================================
            # 3. GENERIC REFERENCE
            # =====================================================

            resolved = self.context.resolve_reference(text)

            if resolved:

                if (
                    "like it" in lower_text
                    or "like this" in lower_text
                    or "like that" in lower_text
                ):

                    response = (
                        f"That's great! You really like "
                        f"{resolved}."
                    )

                elif "good" in lower_text:

                    response = (
                        f"Yes, {resolved} sounds good."
                    )

                else:

                    response = (
                        f"You are referring to {resolved}."
                    )

                self.memory.remember_conversation(
                    "aura",
                    response
                )

                return response

            # =====================================================
            # 4. SEARCH PREVIOUS CONTEXT
            # =====================================================

            relevant_context = (
                self.context.find_relevant_context(text)
            )

            if relevant_context:

                last_context = relevant_context[-1]

                response = (
                    f"I remember you mentioned: "
                    f"{last_context['text']}"
                )

                self.memory.remember_conversation(
                    "aura",
                    response
                )

                return response