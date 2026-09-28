from skills.base import BaseSkill

class CustomSkill(BaseSkill):
    """Template — copy and modify for your own skills."""

    TRIGGER = "your trigger phrase"

    def matches(self, text):
        return self.TRIGGER in text

    def handle(self, text):
        return "Custom skill executed."