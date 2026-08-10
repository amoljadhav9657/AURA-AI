from .short_memory import ShortMemory
from .long_memory import LongMemory


class MemoryManager:

    def __init__(self):
        self.short = ShortMemory(limit=10)
        self.long = LongMemory()

    def remember_conversation(self, role, text):
        self.short.add(role, text)

    def get_conversation(self):
        return self.short.get()

    def clear_conversation(self):
        self.short.clear()

    def last_message(self):
        return self.short.last()

    def remember(self, key, value):
        self.long.save(key, value)

    def recall(self, key):
        return self.long.load(key)
