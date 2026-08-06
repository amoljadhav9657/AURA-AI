"""
=========================================
AURA AI - Browser
Version : 0.6.0
=========================================
"""

import webbrowser


class Browser:

    def __init__(self):
        pass

    def open(self, url):

        try:
            webbrowser.open(url)
            return f"Opening {url}"
        except Exception as e:
            return f"Browser Error : {e}"