class LongMemory:

    def __init__(self):
        self.data = []

    def save(self, text):
        self.data.append(text)

    def load(self):
        return self.data