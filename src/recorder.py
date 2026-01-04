# src/recorder.py - Audio recording module
import threading
import time
from pathlib import Path

import numpy as np
import sounddevice as sd
from scipy.io import wavfile

from .config import SAMPLE_RATE, CHANNELS, TEMP_DIR


class AudioRecorder:
    """Records audio from the microphone and saves to WAV file."""

    def __init__(self):
        self.is_recording = False
        self.audio_data = []
        self.start_time = None
        self._stream = None
        self._lock = threading.Lock()

    def _audio_callback(self, indata, frames, time_info, status):
        """Callback for audio stream - stores audio chunks."""
        if status:
            print(f"Audio status: {status}")
        with self._lock:
            if self.is_recording:
                self.audio_data.append(indata.copy())

    def start_recording(self):
        """Start recording audio from the default microphone."""
        with self._lock:
            if self.is_recording:
                return False

            self.audio_data = []
            self.is_recording = True
            self.start_time = time.time()

        self._stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            callback=self._audio_callback,
            dtype=np.float32,
        )
        self._stream.start()
        return True

    def stop_recording(self) -> tuple[Path | None, float]:
        """
        Stop recording and save to WAV file.

        Returns:
            Tuple of (filepath, duration) or (None, 0) if no audio recorded.
        """
        with self._lock:
            if not self.is_recording:
                return None, 0

            self.is_recording = False
            duration = time.time() - self.start_time if self.start_time else 0

        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None

        with self._lock:
            if not self.audio_data:
                return None, 0

            # Concatenate all audio chunks
            audio = np.concatenate(self.audio_data, axis=0)

        # Convert float32 [-1, 1] to int16
        audio_int16 = (audio * 32767).astype(np.int16)

        # Generate unique filename
        timestamp = int(time.time() * 1000)
        filepath = TEMP_DIR / f"voice_to_claude_{timestamp}.wav"

        # Save WAV file
        wavfile.write(str(filepath), SAMPLE_RATE, audio_int16)

        return filepath, duration

    @property
    def recording(self) -> bool:
        """Check if currently recording."""
        with self._lock:
            return self.is_recording
