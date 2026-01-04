# src/app.py - Voice-to-Claude menubar application
import logging
import os
import subprocess
import threading
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

import rumps

from .config import (
    SOUND_START, SOUND_STOP, SOUND_ERROR,
    LOG_DIR, TRANSCRIPTS_DIR, ensure_dirs
)
from .recorder import AudioRecorder
from .transcriber import Transcriber
from .hotkey import HotkeyManager
from .clipboard import copy_and_paste

# Setup logging
ensure_dirs()
log_file = LOG_DIR / "app.log"
handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3)
handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
))
logging.basicConfig(level=logging.DEBUG, handlers=[handler])
logger = logging.getLogger(__name__)


class VoiceToClaudeApp(rumps.App):
    """Menubar application for voice-to-text transcription."""

    def __init__(self):
        super().__init__(
            name="Voice to Claude",
            title="V",  # Simple text icon
            quit_button=None,  # We'll add our own
        )

        # State
        self.is_recording = False
        self._lock = threading.Lock()

        # Components
        self.recorder = AudioRecorder()
        self.transcriber = None  # Lazy init to catch errors gracefully
        self.hotkey_manager = HotkeyManager(self.toggle_recording)

        # Build menu
        self.status_item = rumps.MenuItem("Status: Idle")
        self.status_item.set_callback(None)  # Not clickable

        self.menu = [
            self.status_item,
            None,  # Separator
            rumps.MenuItem("Toggle Recording (Cmd+Shift+V)", callback=self._menu_toggle),
            None,
            rumps.MenuItem("Open Transcripts Folder", callback=self._open_transcripts),
            rumps.MenuItem("View Logs", callback=self._open_logs),
            None,
            rumps.MenuItem("Quit", callback=self._quit),
        ]

        # Start hotkey listener
        try:
            self.hotkey_manager.start()
        except RuntimeError as e:
            self._notify_error(str(e))

        logger.info("Voice-to-Claude started")

    def _init_transcriber(self) -> bool:
        """Initialize transcriber (lazy loading)."""
        if self.transcriber is not None:
            return True

        try:
            self.transcriber = Transcriber()
            return True
        except FileNotFoundError as e:
            logger.error(f"Transcriber init failed: {e}")
            self._notify_error(str(e))
            return False

    def toggle_recording(self):
        """Toggle recording state."""
        with self._lock:
            if self.is_recording:
                self._stop_recording()
            else:
                self._start_recording()

    def _start_recording(self):
        """Start audio recording."""
        if not self._init_transcriber():
            return

        if self.recorder.start_recording():
            self.is_recording = True
            self._update_status("Recording...", recording=True)
            self._play_sound(SOUND_START)
            logger.info("Recording started")
        else:
            logger.warning("Failed to start recording")

    def _stop_recording(self):
        """Stop recording and transcribe."""
        self._update_status("Transcribing...", recording=False)
        self._play_sound(SOUND_STOP)

        # Stop recording
        audio_path, duration = self.recorder.stop_recording()
        self.is_recording = False

        if not audio_path:
            self._update_status("Idle (no audio)")
            logger.warning("No audio recorded")
            return

        logger.info(f"Recording stopped: {duration:.1f}s")

        # Transcribe in background thread
        threading.Thread(
            target=self._transcribe_and_paste,
            args=(audio_path, duration),
            daemon=True
        ).start()

    def _transcribe_and_paste(self, audio_path: Path, duration: float):
        """Transcribe audio and paste result."""
        try:
            text, language = self.transcriber.transcribe(audio_path)

            if not text:
                self._update_status("Idle (no speech detected)")
                logger.warning("No speech detected in audio")
                return

            # Copy and paste
            if copy_and_paste(text):
                self._update_status("Idle")
                logger.info(f"Transcribed ({language}): {text[:50]}...")

                # Save to history
                self._save_transcript(text, duration, language)

                # Notify success
                self._notify(f"Transcribed: {text[:50]}...")
            else:
                self._update_status("Idle (paste failed)")
                self._play_sound(SOUND_ERROR)

        except Exception as e:
            logger.error(f"Transcription error: {e}")
            self._update_status("Idle (error)")
            self._play_sound(SOUND_ERROR)
            self._notify_error(f"Transcription failed: {e}")

    def _save_transcript(self, text: str, duration: float, language: str):
        """Save transcript to history file."""
        try:
            timestamp = datetime.now()
            filename = timestamp.strftime("%Y-%m-%d_%H-%M-%S.txt")
            filepath = TRANSCRIPTS_DIR / filename

            content = f"""# Voice Transcription
# Date: {timestamp.strftime("%Y-%m-%d %H:%M:%S")}
# Duration: {duration:.1f}s
# Language: {language}

{text}
"""
            filepath.write_text(content)
            logger.debug(f"Saved transcript: {filepath}")

        except Exception as e:
            logger.error(f"Failed to save transcript: {e}")

    def _update_status(self, status: str, recording: bool = False):
        """Update menubar status."""
        self.status_item.title = f"Status: {status}"
        self.title = "V" if not recording else "V*"

    def _play_sound(self, sound_path: str):
        """Play system sound."""
        try:
            subprocess.Popen(
                ["afplay", sound_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception as e:
            logger.warning(f"Failed to play sound: {e}")

    def _notify(self, message: str):
        """Show macOS notification."""
        try:
            import pync
            pync.notify(message, title="Voice to Claude")
        except Exception as e:
            logger.warning(f"Notification failed: {e}")

    def _notify_error(self, message: str):
        """Show error notification."""
        try:
            import pync
            pync.notify(message, title="Voice to Claude - Error")
        except Exception as e:
            logger.warning(f"Error notification failed: {e}")

    def _menu_toggle(self, sender):
        """Menu item callback for toggle."""
        self.toggle_recording()

    def _open_transcripts(self, sender):
        """Open transcripts folder in Finder."""
        subprocess.run(["open", str(TRANSCRIPTS_DIR)])

    def _open_logs(self, sender):
        """Open log file in Console."""
        subprocess.run(["open", "-a", "Console", str(log_file)])

    def _quit(self, sender):
        """Quit the application."""
        logger.info("Quitting Voice-to-Claude")
        self.hotkey_manager.stop()
        rumps.quit_application()


def main():
    """Entry point for the application."""
    app = VoiceToClaudeApp()
    app.run()


if __name__ == "__main__":
    main()
