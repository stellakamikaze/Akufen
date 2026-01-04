# src/transcriber.py - Whisper transcription module
import logging
import os
import subprocess
from pathlib import Path

from .config import WHISPER_CLI, MODEL_PATH, TRANSCRIPTION_TIMEOUT

logger = logging.getLogger(__name__)


class Transcriber:
    """Transcribes audio files using whisper.cpp."""

    def __init__(self, model_path: Path = MODEL_PATH):
        self.model_path = model_path
        self._verify_setup()

    def _verify_setup(self):
        """Verify whisper-cli and model are available."""
        if not Path(WHISPER_CLI).exists():
            raise FileNotFoundError(
                f"whisper-cli not found at {WHISPER_CLI}. "
                "Install with: brew install whisper-cpp"
            )
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model not found at {self.model_path}. "
                "Download from: https://huggingface.co/ggerganov/whisper.cpp"
            )

    def transcribe(self, audio_path: Path, delete_audio: bool = True) -> tuple[str, str]:
        """
        Transcribe audio file to text.

        Args:
            audio_path: Path to WAV audio file.
            delete_audio: If True, delete audio file after transcription.

        Returns:
            Tuple of (transcribed_text, detected_language).
        """
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        try:
            # Run whisper-cli
            result = subprocess.run(
                [
                    WHISPER_CLI,
                    "-m", str(self.model_path),
                    "-f", str(audio_path),
                    "-l", "auto",  # Auto-detect language
                    "-nt",  # No timestamps
                    "-np",  # No prints except result
                ],
                capture_output=True,
                text=True,
                timeout=TRANSCRIPTION_TIMEOUT,
            )

            if result.returncode != 0:
                logger.error(f"Whisper error: {result.stderr}")
                raise RuntimeError(f"Transcription failed: {result.stderr}")

            # Parse output - whisper outputs text to stdout
            text = result.stdout.strip()

            # Clean up common whisper artifacts
            text = self._clean_text(text)

            # Try to detect language from stderr (whisper logs it there)
            language = self._detect_language(result.stderr)

            return text, language

        finally:
            # Clean up audio file
            if delete_audio and audio_path.exists():
                try:
                    os.remove(audio_path)
                    logger.debug(f"Deleted audio file: {audio_path}")
                except OSError as e:
                    logger.warning(f"Failed to delete audio: {e}")

    def _clean_text(self, text: str) -> str:
        """Clean up common whisper transcription artifacts."""
        # Remove common hallucinations
        artifacts = [
            "[BLANK_AUDIO]",
            "[MUSIC]",
            "[APPLAUSE]",
            "(music)",
            "(applause)",
        ]
        for artifact in artifacts:
            text = text.replace(artifact, "")

        # Clean up whitespace
        text = " ".join(text.split())

        return text.strip()

    def _detect_language(self, stderr: str) -> str:
        """Extract detected language from whisper stderr output."""
        # Whisper logs something like: "auto-detected language: it"
        for line in stderr.split("\n"):
            if "language:" in line.lower():
                parts = line.split(":")
                if len(parts) >= 2:
                    return parts[-1].strip()
        return "unknown"
