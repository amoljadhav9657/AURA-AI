class AgentManager:

    def __init__(self):
        self.agents = {
            "developer": "Developer Agent",
            "researcher": "Researcher Agent",
            "debugger": "Debugger Agent",
            "tester": "Tester Agent",
            "analyst": "Data Analyst Agent",
            "desktop": "Desktop Agent",
        }

        self.active_agent = None

        print("🤖 Agent Manager: READY")

    def select_agent(self, command):

        text = command.lower()

        if any(word in text for word in [
            "code",
            "coding",
            "program",
            "develop",
            "software",
            "build",
            "create application",
        ]):
            return "developer"

        if any(word in text for word in [
            "research",
            "search",
            "find information",
            "investigate",
        ]):
            return "researcher"

        if any(word in text for word in [
            "error",
            "bug",
            "debug",
            "fix error",
        ]):
            return "debugger"

        if any(word in text for word in [
            "test",
            "testing",
            "run tests",
        ]):
            return "tester"

        if any(word in text for word in [
            "excel",
            "data",
            "analysis",
            "analytics",
        ]):
            return "analyst"

        if any(word in text for word in [
            "open chrome",
            "open calculator",
            "open notepad",
            "open explorer",
            "open vs code",
            "open vscode",
            "show desktop",
            "system information",
            "system info",
        ]):
            return "desktop"

        return None

    def activate(self, command):

        agent = self.select_agent(command)

        if agent:
            self.active_agent = agent
            print(f"🤖 Active Agent: {self.agents[agent]}")

        return agent

    def status(self):

        return {
            "active_agent": self.active_agent,
            "agents": self.agents,
        }


if __name__ == "__main__":

    manager = AgentManager()

    print()
    print("AURA AGENT MANAGER TEST")
    print("------------------------")

    tests = [
        "create a Python application",
        "research AI agents",
        "fix this error",
        "run tests",
        "analyze my data",
        "open chrome",
    ]

    for command in tests:

        agent = manager.activate(command)

        print(
            f"Command: {command}"
        )

        print(
            f"Agent: {agent}"
        )

        print()
