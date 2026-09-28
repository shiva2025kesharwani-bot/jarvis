import time
import numpy as np
import sounddevice as sd
from openwakeword.model import Model

class WakeWordDetector:
    def __init__(self, config):
        self.threshold = float(config.get("threshold", 0.5))
        self.cooldown = float(config.get("cooldown", 2.0))
        self.last_detection = 0.0
        self.sample_rate = 16000
        self.frame_length = 1280  # openWakeWord needs 80ms chunks

        # Built-in models: hey_jarvis, alexa, hey_mycroft
        self.model = Model(
            wakeword_models=["hey_jarvis"],
            inference_framework="onnx",
        )

    def wait_for_wake_word(self):
        """Block until wake word heard. Always listening."""
        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16",
            blocksize=self.frame_length,
        ) as stream:
            while True:
                frame, _ = stream.read(self.frame_length)
                audio = frame.flatten()
                prediction = self.model.predict(audio)

                for model_name, score in prediction.items():
                    if score > self.threshold:
                        if time.time() - self.last_detection > self.cooldown:
                            self.last_detection = time.time()
                            try:
                                self.model.reset()
                            except Exception:
                                pass
                            return True