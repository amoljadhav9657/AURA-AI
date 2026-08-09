"""
=========================================
AURA AI - System Manager
Version : 0.8.0
=========================================
"""

from .browser import Browser
from .command_parser import CommandParser
from .app_launcher import AppLauncher
from .file_manager import FileManager
from .search_manager import SearchManager


class SystemManager:

    def __init__(self):
        self.browser = Browser()
        self.parser = CommandParser()
        self.apps = AppLauncher()
        self.files = FileManager()
        self.search = SearchManager()

    def execute(self, text):

        command_type, value = self.parser.parse(text)

        # Web Search commands
        if command_type == "search":
            return self.search.search(value)

        # Browser commands
        if command_type == "browser":
            return self.browser.open(value)

        # App commands
        if command_type == "app":
            return self.apps.open(value)

        # Folder commands
        if command_type == "folder":
            return self.files.open(value)

        return None