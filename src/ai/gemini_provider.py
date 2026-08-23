from google import genai
import os

from dotenv import load_dotenv

from .provider import AIProvider


class GeminiProvider(AIProvider):

    def __init__(self):
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured in .env"
            )

        self.client = genai.Client(api_key=api_key)

    def answer(self, text: str) -> str:
        if not text or not text.strip():
            return "Please ask me something."

        response = self.client.models.generate_content(
            model="gemini-3.6-flash",
            contents=text.strip()
        )

        return response.text.strip()

