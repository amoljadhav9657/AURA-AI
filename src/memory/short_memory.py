class ShortMemory:

    def __init__(self, limit=10):
        self.data = []
        self.limit = limit

    def add(self, role, text):
        self.data.append({
            "role": role,
            "text": text
        })

        if len(self.data) > self.limit:
            self.data.pop(0)

    def get(self):
        return self.data.copy()

    def clear(self):
        self.data.clear()

    def last(self):
        if not self.data:
            return None
        return self.data[-1]
