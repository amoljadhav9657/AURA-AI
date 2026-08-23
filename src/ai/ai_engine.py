import os

from dotenv import load_dotenv
from openai import OpenAI


class AIEngine:

    def __init__(self):
        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not configured in .env"
            )

        self.client = OpenAI(api_key=api_key)

    def answer(self, text):
        if not text or not text.strip():
            return "Please ask me something."

        response = self.client.responses.create(
            model="gpt-5.4-mini",
            input=text.strip()
        )

        return response.output_text.strip()