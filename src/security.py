"""
AURA AI Security Foundation
Version: 0.34.0
"""

from urllib.parse import urlparse


class SecurityManager:

    MAX_INPUT_LENGTH = 2000

    SAFE_BROWSER_DOMAINS = {
        "youtube.com",
        "www.youtube.com",
        "google.com",
        "www.google.com",
        "mail.google.com",
        "chat.openai.com",
    }

    BLOCKED_COMMAND_WORDS = {
        "rm ",
        "rm -",
        "sudo ",
        "shutdown",
        "reboot",
        "mkfs",
        "format ",
        "del ",
        "erase ",
        "powershell",
        "cmd.exe",
        "chmod 777",
        "curl ",
        "wget ",
    }

    def validate_input(self, text):
        if not isinstance(text, str):
            return False, "Invalid input."

        text = text.strip()

        if not text:
            return False, "Please say something."

        if len(text) > self.MAX_INPUT_LENGTH:
            return False, "Message is too long."

        return True, None

    def is_dangerous_command(self, text):
        lower = text.lower().strip()

        return any(
            word in lower
            for word in self.BLOCKED_COMMAND_WORDS
        )

    def validate_url(self, url):
        try:
            parsed = urlparse(url)

            if parsed.scheme not in {"http", "https"}:
                return False

            if not parsed.netloc:
                return False

            return True

        except Exception:
            return False

    def is_allowed_browser_url(self, url):
        if not self.validate_url(url):
            return False

        parsed = urlparse(url)
        hostname = (parsed.hostname or "").lower()

        return hostname in self.SAFE_BROWSER_DOMAINS

    def check_text(self, text):
        valid, error = self.validate_input(text)

        if not valid:
            return False, error

        if self.is_dangerous_command(text):
            return (
                False,
                "I can't execute that potentially dangerous command."
            )

        return True, None
