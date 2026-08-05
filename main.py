"""
=========================================
AURA AI
Version : 0.1.0
Founder : Amol Jadhav
=========================================
"""

from src.brain import Brain


class AuraAI:

    def __init__(self):
        self.brain = Brain()

    def start(self):

        print("=" * 60)
        print("🤖 Welcome to AURA AI")
        print("Version : 0.1.0")
        print("Type 'exit' to close AURA AI")
        print("=" * 60)

        while True:

            user_input = input("\nYou : ").strip()

            if not user_input:
                continue

            if user_input.lower() == "exit":
                print("AURA : Goodbye!")
                break

            response = self.brain.process(user_input)

            print("AURA :", response)


def main():
    aura = AuraAI()
    aura.start()


if __name__ == "__main__":
    main()