# src/clipboard.py - Clipboard and paste automation
import logging
import time

import pyperclip
from pynput.keyboard import Controller, Key

from .config import PASTE_DELAY

logger = logging.getLogger(__name__)

# Keyboard controller for simulating key presses
_keyboard = Controller()


def copy_to_clipboard(text: str) -> bool:
    """
    Copy text to system clipboard.

    Args:
        text: Text to copy.

    Returns:
        True if successful, False otherwise.
    """
    try:
        pyperclip.copy(text)
        logger.debug(f"Copied to clipboard: {len(text)} chars")
        return True
    except Exception as e:
        logger.error(f"Failed to copy to clipboard: {e}")
        return False


def paste() -> bool:
    """
    Simulate Cmd+V to paste from clipboard.

    Returns:
        True if successful, False otherwise.
    """
    try:
        _keyboard.press(Key.cmd)
        _keyboard.press('v')
        _keyboard.release('v')
        _keyboard.release(Key.cmd)
        logger.debug("Simulated Cmd+V paste")
        return True
    except Exception as e:
        logger.error(f"Failed to simulate paste: {e}")
        return False


def copy_and_paste(text: str, auto_paste: bool = True) -> bool:
    """
    Copy text to clipboard and optionally paste it.

    Args:
        text: Text to copy and paste.
        auto_paste: If True, automatically paste after copying.

    Returns:
        True if successful, False otherwise.
    """
    if not copy_to_clipboard(text):
        return False

    if auto_paste:
        # Small delay to ensure clipboard is ready
        time.sleep(PASTE_DELAY)
        return paste()

    return True
