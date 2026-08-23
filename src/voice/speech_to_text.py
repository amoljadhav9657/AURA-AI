"""
=========================================
AURA AI - Speech To Text
Version : 0.7.0
=========================================
"""

import speech_recognition as sr


class SpeechToText:

    def __init__(self):

        self.recognizer = sr.Recognizer()

        # Correct laptop microphone
        self.device_index = 1

        # Wake words
        self.wake_words = (
            "hey aura",
            "aura",
        )

        # Recognition settings
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.5

    def listen(self):

        with sr.Microphone(
            device_index=self.device_index
        ) as source:

            print("🎤 Listening...")

            self.recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = self.recognizer.listen(
                source,
                timeout=None,
                phrase_time_limit=8
            )

        try:

            text = self.recognizer.recognize_google(
                audio,
                language="en-IN"
            ).strip()

            if not text:
                return ""

            print("You :", text)

            return text

        except sr.UnknownValueError:

            print("⚠️ Could not understand audio.")
            return ""

        except sr.RequestError as exc:

            print(
                f"⚠️ Speech recognition service error: {exc}"
            )

            return ""

    def listen_for_wake_word(self):

        with sr.Microphone(
            device_index=self.device_index
        ) as source:

            print("🟢 AURA STANDBY")
            print("🎤 Say 'Hey AURA'...")

            self.recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            while True:

                try:

                    audio = self.recognizer.listen(
                        source,
                        timeout=None,
                        phrase_time_limit=5
                    )

                    text = self.recognizer.recognize_google(
                        audio,
                        language="en-IN"
                    ).strip().lower()

                    if not text:
                        continue

                    print("Heard :", text)

                    for wake_word in self.wake_words:

                        if wake_word in text:

                            print("✅ WAKE WORD DETECTED")

                            return True

                except sr.UnknownValueError:

                    continue

                except sr.RequestError as exc:

                    print(
                        f"⚠️ Speech recognition service error: {exc}"
                    )

                    return False
