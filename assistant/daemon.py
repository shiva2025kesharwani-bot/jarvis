import signal
import time
import yaml

from assistant.wake_word import WakeWordDetector
from assistant.stt import SpeechToText
from assistant.tts import TextToSpeech
from assistant.router import CommandRouter
from assistant.audio import AudioRecorder
from assistant.logger import get_logger

log = get_logger("daemon")

def load_config(path="config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def run_daemon():
    config = load_config()

    log.info("Initializing components...")
    wake = WakeWordDetector(config["wake_word"])
    stt = SpeechToText(config["stt"])
    tts = TextToSpeech(config["tts"])
    router = CommandRouter(config)
    recorder = AudioRecorder(config["audio"])
    log.info("All components ready.")

    running = {"flag": True}

    def shutdown(sig, frame):
        log.info("Shutdown signal received.")
        running["flag"] = False

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    log.info("Assistant running. Say 'Hey Buddy' to wake me up.")
    tts.speak("Assistant is ready.")

    while running["flag"]:
        try:
            log.info("Waiting for wake word...")
            wake.wait_for_wake_word()
            log.info("Wake word detected!")

            tts.speak("Yes?")
            time.sleep(0.3)

            log.info("Recording command...")
            audio = recorder.record_until_silence()

            log.info("Transcribing...")
            text = stt.transcribe(audio)

            if not text:
                log.info("Nothing heard.")
                continue

            log.info(f"User: {text}")

            response = router.handle(text)
            log.info(f"Assistant: {response}")

            tts.speak(response)
            time.sleep(0.3)

        except KeyboardInterrupt:
            break
        except Exception as e:
            log.exception(f"Loop error: {e}")
            time.sleep(1)

    log.info("Assistant stopped.")