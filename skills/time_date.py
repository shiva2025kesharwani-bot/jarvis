import datetime
from skills.base import BaseSkill

class TimeDateSkill(BaseSkill):
    def matches(self, text):
        keywords = ["time", "date", "day", "today", "what's the"]
        return any(k in text for k in keywords) and any(
            k in text for k in ["time", "date", "day", "today"]
        )

    def handle(self, text):
        now = datetime.datetime.now()
        if "time" in text:
            return f"The current time is {now.strftime('%I:%M %p').lstrip('0')}."
        if "date" in text or "today" in text or "day" in text:
            return f"Today is {now.strftime('%A, %B %d, %Y')}."
        return f"It is {now.strftime('%A, %I:%M %p')} on {now.strftime('%B %d, %Y')}."