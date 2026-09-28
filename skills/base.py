class BaseSkill:
    def matches(self, text: str) -> bool:
        raise NotImplementedError

    def handle(self, text: str) -> str:
        raise NotImplementedError