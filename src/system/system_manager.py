"""
=========================================
AURA AI - System Manager
Version : 0.6.0
=========================================
"""

from .browser import Browser
from .command_parser import CommandParser


class SystemManager:

    def __init__(self):
        self.browser = Browser()
        self.parser = CommandParser()

    def execute(self, text):

        command_type, value = self.parser.parse(text)

        if command_type == "browser":
            return self.browser.open(value)

        return None