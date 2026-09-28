import webbrowser
import urllib.parse
from skills.base import BaseSkill

class WebSearchSkill(BaseSkill):
    def matches(self, text):
        triggers = [
            "search", "google", "look up", "find",
            "search for", "search the web for",
            "browse", "web search",
        ]
        return any(t in text for t in triggers)

    def handle(self, text):
        # Strip trigger words
        query = text
        for trigger in [
            "search the web for", "search for", "search on google",
            "search on", "look up", "find", "search", "google", "browse",
        ]:
            query = query.replace(trigger, "", 1).strip()

        if not query:
            return "What should I search for?"

        url = "https://www.google.com/search?q=" + urllib.parse.quote(query)
        webbrowser.open(url)
        return f"Searching the web for {query}."