import pyttsx3

class TextToSpeech:
    def __init__(self, config):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 175)
        self.engine.setProperty("volume", 1.0)

        # Best available voice pick karo (Zira/David/Heera)
        voices = self.engine.getProperty("voices")
        if voices:
            self.engine.setProperty("voice", voices[0].id)

    def speak(self, text):
        if not text or not text.strip():
            return
        print(f"🔊 Speaking: {text}", flush=True)
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except RuntimeError:
            self.engine = pyttsx3.init()
            self.engine.say(text)
            self.engine.runAndWait()