print("1. started")
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
print("2. path set")

from dotenv import load_dotenv
load_dotenv()
print("3. env loaded")

import yaml
config = yaml.safe_load(open("config.yaml"))
print("4. config loaded")
print("   wake word:", config["wake_word"]["wake_word"])

from assistant.wake_word import WakeWordDetector
print("5. wake_word imported")

from assistant.stt import SpeechToText
print("6. stt imported")

from assistant.tts import TextToSpeech
print("7. tts imported")

from assistant.router import CommandRouter
print("8. router imported")

from assistant.audio import AudioRecorder
print("9. audio imported")

from assistant.daemon import run_daemon
print("10. daemon imported")

print("ALL OK")