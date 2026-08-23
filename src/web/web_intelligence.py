from ddgs import DDGS


class WebIntelligence:

    def search(self, query: str, max_results: int = 5) -> str:

        if not query or not query.strip():
            return "Please provide a search query."

        results = []

        try:
            with DDGS() as ddgs:
                search_results = ddgs.text(
                    query.strip(),
                    max_results=max_results
                )

                for item in search_results:
                    title = item.get("title", "")
                    body = item.get("body", "")
                    href = item.get("href", "")

                    results.append(
                        f"TITLE: {title}\n"
                        f"SUMMARY: {body}\n"
                        f"URL: {href}"
                    )

        except Exception as e:
            return f"Web search failed: {e}"

        if not results:
            return "No web results found."

        return "\n\n".join(results)