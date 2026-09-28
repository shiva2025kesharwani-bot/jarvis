import time
import numpy as np
import sounddevice as sd

class AudioRecorder:
    def __init__(self, config):
        self.sample_rate = int(config["sample_rate"])
        self.frame_length = int(config["frame_length"])
        self.silence_threshold = int(config["silence_threshold"])
        self.silence_duration = float(config["silence_duration"])
        self.max_record_seconds = float(config["max_record_seconds"])

    def record_until_silence(self):
        frames = []
        silence_frames = 0
        silence_limit = int(self.silence_duration * self.sample_rate / self.frame_length)
        max_frames = int(self.max_record_seconds * self.sample_rate / self.frame_length)

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16",
            blocksize=self.frame_length,
        ) as stream:
            # Pre-roll: capture 1 second before real recording
            # so we don't miss the first word
            pre_roll_frames = int(1.0 * self.sample_rate / self.frame_length)
            for _ in range(pre_roll_frames):
                frame, _ = stream.read(self.frame_length)
                frames.append(frame.copy())

            # Now record actively until silence
            for _ in range(max_frames):
                frame, _ = stream.read(self.frame_length)
                frames.append(frame.copy())
                rms = int(np.sqrt(np.mean(frame.astype(np.float32) ** 2)))
                if rms < self.silence_threshold:
                    silence_frames += 1
                else:
                    silence_frames = 0
                if silence_frames > silence_limit and len(frames) > pre_roll_frames + 5:
                    break

        if not frames:
            return np.zeros(0, dtype=np.int16)
        return np.concatenate(frames, axis=0).flatten()