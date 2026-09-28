import requests
from assistant.logger import get_logger

log = get_logger("llm")

class LLMService:
    def __init__(self, config):
        self.enabled = bool(config.get("enabled", False))
        self.provider = config.get("provider", "ollama")
        self.model = config.get("model", "llama3.2:3b")
        self.url = config.get("url", "http://localhost:11434/api/chat")
        self.system_prompt = config.get("system_prompt", "You are a helpful assistant.")
        self.history = [{"role": "system", "content": self.system_prompt}]

    def query(self, text):
        if not self.enabled:
            return "I'm not sure how to help with that yet."

        self.history.append({"role": "user", "content": text})

        # Keep only last 10 messages (plus system) to avoid bloat
        if len(self.history) > 11:
            self.history = [self.history[0]] + self.history[-10:]

        try:
            log.info(f"Querying Ollama model: {self.model}")
            r = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "messages": self.history,
                    "stream": False,
                    "options": {
                        "temperature": 0.8,
                        "num_predict": 120,
                    },
                },
                timeout=90,
            )
            if r.status_code != 200:
                log.error(f"Ollama error: {r.status_code} - {r.text}")
                return "I couldn't think properly, sorry."

            reply = r.json().get("message", {}).get("content", "").strip()
            if not reply:
                return "I'm not sure what to say."

            self.history.append({"role": "assistant", "content": reply})
            log.info(f"LLM reply: {reply}")
            return reply

        except requests.exceptions.ConnectionError:
            log.error("Ollama not reachable. Is it running?")
            return "I can't reach my brain. Please check if Ollama is running."
        except Exception as e:
            log.exception(f"LLM error: {e}")
            return "Something went wrong in my head."