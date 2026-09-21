"""
AURA AI - Chrome Browser Controller
Opens AURA web commands directly in Google Chrome on Windows.
"""

import os
import shutil
import subprocess
from pathlib import Path


class Browser:

    def __init__(self):
        self.chrome_path = self._find_chrome()

    def _find_chrome(self):
        # 1. PATH
        chrome = shutil.which("chrome")
        if chrome:
            return chrome

        # 2. Common Windows Chrome installations
        candidates = [
            os.path.expandvars(
                r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"
            ),
            os.path.expandvars(
                r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
            ),
            os.path.expandvars(
                r"%LocalAppData%\Google\Chrome\Application\chrome.exe"
            ),
            os.path.expandvars(
                r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
            ),
        ]

        for path in candidates:
            if Path(path).is_file():
                return path

        return None

    def open(self, url):
        if not url:
            return "No website URL provided."

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        if not self.chrome_path:
            return (
                "Google Chrome was not found on this Windows system. "
                "Please install Chrome or check the Chrome installation path."
            )

        try:
            subprocess.Popen(
                [self.chrome_path, "--new-window", url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=getattr(
                    subprocess,
                    "CREATE_NO_WINDOW",
                    0
                ),
            )

            return f"Opening {url} in Google Chrome."

        except Exception as exc:
            return f"Unable to open Google Chrome: {exc}"
