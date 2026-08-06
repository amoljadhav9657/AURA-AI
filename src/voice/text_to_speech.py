"""
=========================================
AURA AI - Text To Speech
Version : 0.4.0
=========================================
"""

import pyttsx3


class TextToSpeech:

    def __init__(self):
        self.engine = None

        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", 170)
            self.engine.setProperty("volume", 1.0)
        except Exception as e:
            print("[Voice Error]", e)

    def speak(self, text):
        print("AURA :", text)

        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print("[Voice Warning]", e)