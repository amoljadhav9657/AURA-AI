from src.database import Database


class LongMemory:

    def __init__(self):
        self.db = Database()

    def save(self, key, value):
        self.db.save_memory(key, value)

    def load(self, key):
        return self.db.load_memory(key)

    def get_all(self):
        return self.db.get_all_memories()