import io
import time
import wave
import speech_recognition as sr

class SpeechToText:
    def __init__(self, config):
        self.recognizer = sr.Recognizer()
        self.sample_rate = 16000
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

    def _audio_to_wav(self, audio_int16):
        buf = io.BytesIO()
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_int16.tobytes())
        buf.seek(0)
        return buf

    def transcribe(self, audio_int16):
        if audio_int16 is None or len(audio_int16) == 0:
            return ""

        buf = self._audio_to_wav(audio_int16)

        # Retry logic for network errors
        for attempt in range(3):
            try:
                with sr.AudioFile(buf) as source:
                    audio = self.recognizer.record(source)

                text = self.recognizer.recognize_google(audio, language="en-IN")
                print(f"   [Google STT heard]: '{text}'", flush=True)
                return text

            except sr.UnknownValueError:
                print("   [Google STT] Could not understand", flush=True)
                return ""

            except sr.RequestError as e:
                print(f"   [Google STT] Network error (attempt {attempt+1}/3): {e}", flush=True)
                if attempt < 2:
                    time.sleep(1.5)
                    buf = self._audio_to_wav(audio_int16)  # reset buffer
                    continue
                return ""

            except Exception as e:
                print(f"   [Google STT] Error: {e}", flush=True)
                return ""

        return ""