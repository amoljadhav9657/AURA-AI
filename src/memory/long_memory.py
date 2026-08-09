"""
=========================================
AURA AI - Long Memory
Version : 0.11.0
=========================================
"""

from src.database import Database


class LongMemory:

    def __init__(self):
        self.db = Database()

    def save(self, key, value):
        self.db.save_memory(key, value)

    def load(self, key):
        return self.db.load_memory(key)