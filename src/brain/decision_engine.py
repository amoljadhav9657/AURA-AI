"""
=========================================
AURA AI - Decision Engine
Version : 0.1.0
=========================================
"""

from datetime import datetime


class DecisionEngine:

    def execute(self, intent: str) -> str:

        if intent == "greeting":
            return "Hello! I am AURA AI."

        elif intent == "time":
            return datetime.now().strftime("Current Time : %I:%M %p")

        elif intent == "date":
            return datetime.now().strftime("Today's Date : %d-%m-%Y")

        else:
            return "Sorry, I don't understand."