"""
=========================================
AURA AI - Text To Speech
Version : 0.7.0
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

            voices = self.engine.getProperty("voices")

            # Microsoft Zira = Female English voice
            for v in voices:
                if "Zira" in v.name:
                    self.engine.setProperty("voice", v.id)
                    break

            self.engine.setProperty("rate", 165)
            self.engine.setProperty("volume", 1.0)

            print("[TTS] Female voice: Microsoft Zira")

        except Exception as e:
            print("[TTS Error]", e)
            self.engine = None

    def speak(self, text):

        if not self.engine:
            return

        if not text:
            return

        try:
            

            self.engine.say(text)
            self.engine.runAndWait()

        except Exception as e:
            print("[TTS Warning]", e)