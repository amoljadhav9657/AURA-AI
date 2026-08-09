"""
=========================================
AURA AI - Search Manager
Version : 0.8.0
=========================================
"""

import urllib.parse

from .browser import Browser


class SearchManager:

    def __init__(self):
        self.browser = Browser()

    def search(self, query):

        query = query.strip()

        if not query:
            return "What would you like me to search for?"

        encoded_query = urllib.parse.quote_plus(query)

        url = f"https://www.google.com/search?q={encoded_query}"

        result = self.browser.open(url)

        return result