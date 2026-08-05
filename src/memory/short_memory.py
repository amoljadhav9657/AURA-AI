class ShortMemory:

    def __init__(self):
        self.data = []

    def add(self, text):
        self.data.append(text)

    def get(self):
        return self.data