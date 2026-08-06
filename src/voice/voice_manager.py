"""
=========================================
AURA AI - Voice Manager
Version : 0.5.0
=========================================
"""

from .text_to_speech import TextToSpeech
from .speech_to_text import SpeechToText


class VoiceManager:

    def __init__(self):
        self.tts = TextToSpeech()
        self.stt = SpeechToText()

    def speak(self, text):
        self.tts.speak(text)

    def listen(self):
        return self.stt.listen()