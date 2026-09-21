"""
=========================================
AURA AI - App Launcher
Version : 0.8.0
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

            "vscode": {
                "linux": "code",
                "windows": "code.cmd",
            },
        }

    def open(self, app_name):

        app_name = app_name.lower().strip()

        if app_name not in self.apps:
            return f"Unknown application: {app_name}"

        # =========================================
        # WINDOWS
        # =========================================

        if os.name == "nt":

            command = self.apps[app_name]["windows"]

            # Special handling for VS Code
            if app_name == "vscode":

                code_cmd = shutil.which("code.cmd")

                if not code_cmd:
                    code_cmd = (
                        r"C:\Users\HP\AppData\Local\Programs"
                        r"\Microsoft VS Code\bin\code.cmd"
                    )

                if not os.path.isfile(code_cmd):
                    return (
                        "VS Code was not found. "
                        "Please check the VS Code installation."
                    )

                try:
                    subprocess.Popen(
                        ["cmd.exe", "/c", code_cmd],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        creationflags=getattr(
                            subprocess,
                            "CREATE_NO_WINDOW",
                            0
                        )
                    )

                    return "Opening Visual Studio Code."

                except Exception as e:
                    return f"VS Code Launcher Error : {e}"

            # Normal Windows applications
            try:

                subprocess.Popen(
                    [command],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=getattr(
                        subprocess,
                        "CREATE_NO_WINDOW",
                        0
                    )
                )

                return f"Opening {app_name.title()}"

            except Exception as e:
                return f"App Launcher Error : {e}"

        # =========================================
        # LINUX
        # =========================================

        command = self.apps[app_name]["linux"]

        if shutil.which(command) is None:
            return (
                f"{app_name.title()} is not available "
                "in this environment."
            )

        try:

            subprocess.Popen(
                [command],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            return f"Opening {app_name.title()}"

        except Exception as e:
            return f"App Launcher Error : {e}"