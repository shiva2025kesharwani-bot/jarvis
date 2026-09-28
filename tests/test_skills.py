import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from skills.time_date import TimeDateSkill
from skills.weather import WeatherSkill
from skills.open_app import OpenAppSkill

def test_time_match():
    assert TimeDateSkill().matches("what time is it")

def test_weather_match():
    assert WeatherSkill().matches("what's the weather")

def test_open_match():
    assert OpenAppSkill().matches("open notepad")

if __name__ == "__main__":
    test_time_match()
    test_weather_match()
    test_open_match()
    print("All skill tests passed.")