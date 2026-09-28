import requests
from skills.base import BaseSkill

# Default city; user can change
DEFAULT_CITY = "London"

class WeatherSkill(BaseSkill):
    def matches(self, text):
        return "weather" in text or "temperature" in text

    def handle(self, text):
        # Free, no-key weather service (open-meteo)
        try:
            geo = requests.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": DEFAULT_CITY, "count": 1},
                timeout=5,
            ).json()

            if not geo.get("results"):
                return "I couldn't find that city."

            lat = geo["results"][0]["latitude"]
            lon = geo["results"][0]["longitude"]
            name = geo["results"][0]["name"]

            weather = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={"latitude": lat, "longitude": lon, "current_weather": True},
                timeout=5,
            ).json()

            cur = weather.get("current_weather", {})
            temp = cur.get("temperature")
            wind = cur.get("windspeed")
            return f"Currently in {name} it's {temp} degrees Celsius with wind at {wind} km/h."
        except Exception:
            return "Sorry, I couldn't fetch the weather right now."