"""
=========================================
AURA AI Command Parser
Version : 0.9.0
=========================================
"""


class CommandParser:

    def parse(self, command):

        command = command.lower().strip()

        # Web Search
        search_prefixes = [
            "search for ",
            "search ",
            "find ",
            "look up "
        ]

        for prefix in search_prefixes:

            if command.startswith(prefix):

                query = command[len(prefix):].strip()

                if query:
                    return ("search", query)

        # Google Search
        if command.startswith("google "):

            query = command[7:].strip()

            if query:
                return ("search", query)

        # Browser Commands
        browser_commands = {
            "youtube": [
                "open youtube",
                "go to youtube",
                "launch youtube"
            ],
            "google": [
                "open google",
                "go to google",
                "launch google"
            ],
            "gmail": [
                "open gmail",
                "go to gmail",
                "launch gmail"
            ],
            "chatgpt": [
                "open chatgpt",
                "go to chatgpt",
                "launch chatgpt"
            ]
        }

        browser_urls = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "gmail": "https://mail.google.com",
            "chatgpt": "https://chat.openai.com"
        }

        for site, commands in browser_commands.items():

            if command in commands:
                return ("browser", browser_urls[site])

        # Apps
        if "calculator" in command:
            return ("app", "calculator")

        elif "notepad" in command:
            return ("app", "notepad")

        elif "paint" in command:
            return ("app", "paint")

        elif "explorer" in command:
            return ("app", "explorer")

        # Folders
        if "downloads" in command:
            return ("folder", "downloads")

        elif "documents" in command:
            return ("folder", "documents")

        elif "desktop" in command:
            return ("folder", "desktop")

        return ("chat", command)