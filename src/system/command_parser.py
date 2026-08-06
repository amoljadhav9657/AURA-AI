"""
=========================================
AURA AI Command Parser
Version : 0.6.0
=========================================
"""


class CommandParser:

    def parse(self, command):

        command = command.lower().strip()

        # Browser
        if "youtube" in command:
            return ("browser", "https://www.youtube.com")

        elif "google" in command:
            return ("browser", "https://www.google.com")

        elif "gmail" in command:
            return ("browser", "https://mail.google.com")

        elif "chatgpt" in command:
            return ("browser", "https://chat.openai.com")

        # Apps
        elif "notepad" in command:
            return ("app", "notepad")

        elif "calculator" in command:
            return ("app", "calculator")

        elif "paint" in command:
            return ("app", "paint")

        elif "explorer" in command:
            return ("app", "explorer")

        # Folders
        elif "documents" in command:
            return ("folder", "documents")

        elif "downloads" in command:
            return ("folder", "downloads")

        elif "desktop" in command:
            return ("folder", "desktop")

        return ("chat", command)