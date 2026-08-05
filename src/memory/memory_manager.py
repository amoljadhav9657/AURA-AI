from .short_memory import ShortMemory
from .long_memory import LongMemory


class MemoryManager:

    def __init__(self):
        self.short = ShortMemory()
        self.long = LongMemory()

    def remember(self, text):
        self.short.add(text)
        self.long.save(text)