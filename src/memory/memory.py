class Memory:

    def __init__(self):
        self.facts = {}

    def remember(self, key, value):
        self.facts[key] = value

    def recall(self, key):
        return self.facts.get(key)