from .text_to_speech import TextToSpeech


class VoiceManager:

    def __init__(self):
        self.tts = TextToSpeech()

    def speak(self, text):
        self.tts.speak(text)