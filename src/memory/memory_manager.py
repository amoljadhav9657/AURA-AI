"""
=========================================
AURA AI - Memory Manager
Version : 0.11.0
=========================================
"""

from .short_memory import ShortMemory
from .long_memory import LongMemory


class MemoryManager:

    def __init__(self):
        self.short = ShortMemory()
        self.long = LongMemory()

    def remember(self, key, value):

        self.short.add(f"{key}: {value}")
        self.long.save(key, value)

    def recall(self, key):

        return self.long.load(key)