"""
=========================================
AURA AI - App Launcher
Version : 0.7.0
=========================================
"""

import os
import shutil
import subprocess


class AppLauncher:

    def __init__(self):
        self.apps = {
            "calculator": {
                "linux": "gnome-calculator",
                "windows": "calc.exe",
            },
            "notepad": {
                "linux": "gedit",
                "windows": "notepad.exe",
            },
            "paint": {
                "linux": "pinta",
                "windows": "mspaint.exe",
            },
            "explorer": {
                "linux": "nautilus",
                "windows": "explorer.exe",
            },
        }

    def open(self, app_name):

        app_name = app_name.lower().strip()

        if app_name not in self.apps:
            return f"Unknown application: {app_name}"

        if os.name == "nt":
            command = self.apps[app_name]["windows"]
        else:
            command = self.apps[app_name]["linux"]

        # Check whether Linux application exists
        if os.name != "nt" and shutil.which(command) is None:
            return f"{app_name.title()} is not available in this environment."

        try:
            subprocess.Popen(
                [command],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            return f"Opening {app_name.title()}"

        except Exception as e:
            return f"App Launcher Error : {e}"