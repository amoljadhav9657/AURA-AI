"""
=========================================
AURA AI - Text To Speech
Version : 0.6.0
=========================================
"""

import pyttsx3
from src.config import VOICE_ENABLED


class TextToSpeech:

    def __init__(self):
        self.engine = None

        if not VOICE_ENABLED:
            return

        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", 170)
            self.engine.setProperty("volume", 1.0)
        except Exception as e:
            print("[Voice Error]", e)

    def speak(self, text):

        if not self.engine:
            return

        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print("[Voice Warning]", e)