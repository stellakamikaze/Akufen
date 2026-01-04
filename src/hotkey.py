# src/hotkey.py - Global hotkey handler
import logging
import threading
from typing import Callable

from pynput import keyboard

from .config import HOTKEY_COMBO

logger = logging.getLogger(__name__)


class HotkeyManager:
    """Manages global hotkey registration and callbacks."""

    def __init__(self, on_toggle: Callable[[], None]):
        """
        Initialize hotkey manager.

        Args:
            on_toggle: Callback function to call when hotkey is pressed.
        """
        self.on_toggle = on_toggle
        self._listener = None
        self._hotkey = None

    def start(self):
        """Start listening for global hotkey."""
        try:
            self._hotkey = keyboard.GlobalHotKeys({
                HOTKEY_COMBO: self._on_hotkey_pressed
            })
            self._hotkey.start()
            logger.info(f"Hotkey listener started: {HOTKEY_COMBO}")
        except Exception as e:
            logger.error(f"Failed to start hotkey listener: {e}")
            raise RuntimeError(
                "Failed to register hotkey. "
                "Please grant Accessibility permission in "
                "System Preferences > Privacy & Security > Accessibility"
            )

    def stop(self):
        """Stop listening for hotkey."""
        if self._hotkey:
            self._hotkey.stop()
            self._hotkey = None
            logger.info("Hotkey listener stopped")

    def _on_hotkey_pressed(self):
        """Called when hotkey combination is pressed."""
        logger.debug("Hotkey pressed")
        # Run callback in separate thread to not block hotkey listener
        threading.Thread(target=self.on_toggle, daemon=True).start()
