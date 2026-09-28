from skills.time_date import TimeDateSkill
from skills.weather import WeatherSkill
from skills.open_app import OpenAppSkill
from skills.web_search import WebSearchSkill
from skills.music import MusicSkill
from services.llm import LLMService
from assistant.logger import get_logger

log = get_logger("router")

class CommandRouter:
    def __init__(self, config):
        self.config = config
        self.skills = [
            TimeDateSkill(),
            OpenAppSkill(),
            WebSearchSkill(),
            MusicSkill(),
            WeatherSkill(),
        ]
        self.llm = LLMService(config.get("llm", {}))

    def handle(self, text: str) -> str:
        text_l = text.lower().strip()
        if not text_l:
            return ""

        # 1. Try specific skills first (fast, deterministic)
        for skill in self.skills:
            try:
                if skill.matches(text_l):
                    log.info(f"Skill matched: {skill.__class__.__name__}")
                    return skill.handle(text_l)
            except Exception as e:
                log.exception(f"Skill error: {e}")

        # 2. Fall back to LLM (friend mode for conversations)
        log.info(f"→ LLM (friend mode): {text}")
        return self.llm.query(text)