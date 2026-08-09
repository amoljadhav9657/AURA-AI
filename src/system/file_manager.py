"""
=========================================
AURA AI - File Manager
Version : 0.7.0
=========================================
"""

import os


class FileManager:

    def __init__(self):
        self.folders = {
            "downloads": os.path.expanduser("~/Downloads"),
            "documents": os.path.expanduser("~/Documents"),
            "desktop": os.path.expanduser("~/Desktop"),
        }

    def open(self, folder_name):

        folder_name = folder_name.lower().strip()

        if folder_name not in self.folders:
            return f"Unknown folder: {folder_name}"

        folder_path = self.folders[folder_name]

        if not os.path.exists(folder_path):
            return f"{folder_name.title()} folder is not available in this environment."

        try:
            os.system(f'xdg-open "{folder_path}"')
            return f"Opening {folder_name.title()}"

        except Exception as e:
            return f"File Manager Error : {e}"