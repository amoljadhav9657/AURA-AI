"""
=========================================
AURA AI
Version : 0.37.0
Founder : Amol Jadhav
=========================================
"""

from src.brain import Brain
from src.voice.voice_manager import VoiceManager
from src.config import APP_NAME, VERSION
from src.face.face_auth import FaceAuthManager


class AuraAI:

    def __init__(self):
        # Face authentication MUST happen before AURA components are created.
        self.face_auth = FaceAuthManager()

        self.brain = None
        self.voice = None

    def authenticate_startup(self):

        print("\n" + "=" * 60)
        print("🔐 AURA AI SECURITY")
        print("=" * 60)

        print("📷 Camera / Face Authentication required.")
        print("AURA will remain LOCKED until the authorized face is verified.")

        # Do not allow a startup bypass.
        if not self.face_auth.is_available():
            print("\n❌ AURA LOCKED")
            print("Face authentication system is not available.")
            return False

        result = self.face_auth.authenticate()

        if not result.get("authenticated", False):
            print("\n❌ AURA LOCKED")
            print("Face authentication failed.")
            return False

        print("\n✅ FACE AUTHENTICATED")
        print(f"👤 User : {result.get('user')}")
        print("🔓 AURA UNLOCKED")

        return True

    def start(self):

        # SECURITY GATE
        if not self.authenticate_startup():
            return

        # Only create Brain / Voice after successful authentication.
        self.brain = Brain()
        self.voice = VoiceManager()

        print("\n" + "=" * 60)
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
                self.face_auth.lock()
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
                self.face_auth.lock()
                break

            response = self.brain.process(user_input)

            self.voice.speak(response)


def main():
    aura = AuraAI()
    aura.start()


if __name__ == "__main__":
    main()
