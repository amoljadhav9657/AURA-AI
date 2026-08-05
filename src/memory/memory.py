"""
=========================================
AURA AI Memory
Version : 0.3.0
=========================================
"""

from src.database import Database


class Memory:

    def __init__(self):
        self.db = Database()

    def remember(self, key, value):
        self.db.save_memory(key, value)

    def recall(self, key):
        return self.db.load_memory(key)