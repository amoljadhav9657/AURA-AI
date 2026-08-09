"""
=========================================
AURA AI
Version : 0.7.0
Founder : Amol Jadhav
=========================================
"""

from src.brain import Brain
from src.voice.voice_manager import VoiceManager
from src.config import APP_NAME, VERSION


class AuraAI:

    def __init__(self):
        self.brain = Brain()
        self.voice = VoiceManager()

    def start(self):

        print("=" * 60)
        print(f"🤖 Welcome to {APP_NAME}")
        print(f"Version : {VERSION}")
        print("=" * 60)

        print("\nSelect Mode")
        print("1. Keyboard Mode")
        print("2. Voice Mode")

        choice = input("\nChoice : ").strip()

        if choice == "2":
            self.voice_mode()
        else:
            self.keyboard_mode()

    def keyboard_mode(self):

        print("\n⌨️ Keyboard Mode Started")
        print("Type 'exit' to close AURA AI")

        while True:

            user_input = input("\nYou : ").strip()

            if not user_input:
                continue

            if user_input.lower() == "exit":
                print("AURA : Goodbye!")
                break

            response = self.brain.process(user_input)

            print("AURA :", response)

            self.voice.speak(response)

    def voice_mode(self):

        print("\n🎤 Voice Mode Started")
        print("Say 'exit' to close AURA AI")

        while True:

            user_input = self.voice.listen()

            if not user_input:
                continue

            if user_input.lower() == "exit":
                self.voice.speak("Goodbye!")
                break

            response = self.brain.process(user_input)

            self.voice.speak(response)


def main():
    aura = AuraAI()
    aura.start()


if __name__ == "__main__":
    main()