# src/config.py - Configuration constants for Voice-to-Claude
import os
from pathlib import Path

# Paths
HOME = Path.home()
MODEL_PATH = HOME / ".local/share/whisper-cpp/models/ggml-large-v3.bin"
WHISPER_CLI = "/opt/homebrew/bin/whisper-cli"
TEMP_DIR = Path("/tmp")
TRANSCRIPTS_DIR = HOME / "Documents/voice-transcripts"
LOG_DIR = HOME / "Library/Logs/voice-to-claude"

# Audio settings
SAMPLE_RATE = 16000  # Whisper requires 16kHz
CHANNELS = 1  # Mono

# Hotkey
HOTKEY_COMBO = "<cmd>+<shift>+v"

# Timing
PASTE_DELAY = 0.1  # seconds between copy and paste
TRANSCRIPTION_TIMEOUT = 60  # seconds

# System sounds (macOS)
SOUND_START = "/System/Library/Sounds/Tink.aiff"
SOUND_STOP = "/System/Library/Sounds/Pop.aiff"
SOUND_ERROR = "/System/Library/Sounds/Basso.aiff"

# Ensure directories exist
def ensure_dirs():
    """Create required directories if they don't exist."""
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
