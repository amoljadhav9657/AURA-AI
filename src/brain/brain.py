"""
=========================================
AURA AI - Brain Module
Version : 0.1.0
=========================================
"""

from .intent_classifier import IntentClassifier
from .decision_engine import DecisionEngine


class Brain:

    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.decision_engine = DecisionEngine()

    def process(self, user_input: str) -> str:

        intent = self.intent_classifier.detect(user_input)

        response = self.decision_engine.execute(intent)

        return response