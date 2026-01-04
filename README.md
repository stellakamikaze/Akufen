# Voice-to-Claude

Menubar app for macOS that enables voice dictation with local Whisper transcription. Dictate text and have it automatically pasted into any application.

## Features

- Global hotkey (Cmd+Shift+V) to start/stop recording
- Local transcription using whisper.cpp (no cloud, no API keys)
- Automatic language detection (Italian, English, and more)
- Audio feedback (system sounds)
- Automatic paste into active application
- Transcript history saved to disk
- Native macOS notifications
- Launch at login support

## Requirements

- macOS 11+ (Big Sur or later)
- Apple Silicon (M1/M2/M3) or Intel Mac
- Python 3.10+
- Homebrew

## Installation

### 1. Install whisper.cpp

```bash
brew install whisper-cpp
```

### 2. Download the model

```bash
mkdir -p ~/.local/share/whisper-cpp/models
curl -L "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3.bin" \
    -o ~/.local/share/whisper-cpp/models/ggml-large-v3.bin
```

This is a ~3GB download and may take a while.

### 3. Clone and setup

```bash
git clone https://github.com/stellakamikaze/voice-to-claude.git
cd voice-to-claude
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Grant permissions

Before running, you need to grant permissions in **System Preferences > Privacy & Security**:

1. **Accessibility**: Add your terminal app (Terminal.app, iTerm2, etc.)
2. **Microphone**: Allow access when prompted

### 5. Run

```bash
source .venv/bin/activate
python -m src.app
```

A "V" icon will appear in your menubar.

## Usage

1. Press **Cmd+Shift+V** to start recording (you'll hear a "tink" sound)
2. Speak into your microphone
3. Press **Cmd+Shift+V** again to stop (you'll hear a "pop" sound)
4. Wait for transcription (the menubar will show "Transcribing...")
5. The text will be automatically pasted into your active application

## Launch at Login

To start Voice-to-Claude automatically at login:

```bash
cp scripts/com.voicetoclaude.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.voicetoclaude.plist
```

To disable:

```bash
launchctl unload ~/Library/LaunchAgents/com.voicetoclaude.plist
rm ~/Library/LaunchAgents/com.voicetoclaude.plist
```

## Files

- **Logs**: `~/Library/Logs/voice-to-claude/app.log`
- **Transcripts**: `~/Documents/voice-transcripts/`

## Troubleshooting

### Hotkey doesn't work

Make sure your terminal/app has Accessibility permission in System Preferences.

### No audio recorded

Check Microphone permission in System Preferences.

### Transcription is slow

The large-v3 model provides the best accuracy but takes ~10-30 seconds for longer recordings. You can switch to a smaller model (medium, small) for faster results at the cost of accuracy.

### Model not found

Ensure the model is downloaded to `~/.local/share/whisper-cpp/models/ggml-large-v3.bin`

## License

MIT

## Credits

- [whisper.cpp](https://github.com/ggerganov/whisper.cpp) - C/C++ port of OpenAI's Whisper
- [rumps](https://github.com/jaredks/rumps) - Ridiculously Uncomplicated macOS Python Statusbar apps
