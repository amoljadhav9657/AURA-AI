from .speech_to_text import SpeechToText


class WakeWord:

    def __init__(self):
        self.stt = SpeechToText()

    def wait(self):
        return self.stt.listen_for_wake_word()
