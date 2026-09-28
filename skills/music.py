import webbrowser
import urllib.parse
from skills.base import BaseSkill

class MusicSkill(BaseSkill):
    def matches(self, text):
        return "play" in text and ("music" in text or "song" in text or "youtube" in text)

    def handle(self, text):
        song = text.replace("play", "").replace("music", "").replace("on youtube", "").strip()
        if not song:
            webbrowser.open("https://www.youtube.com")
            return "Opening YouTube."
        url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(song)
        webbrowser.open(url)
        return f"Playing {song} on YouTube."