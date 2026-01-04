# voice-to-claude

Menubar app macOS per dettatura vocale con trascrizione Whisper locale.

## Stack

- **Python 3.13+** con rumps (menubar)
- **whisper.cpp** per trascrizione locale (Metal GPU)
- **Modello:** ggml-large-v3

## Comandi

```bash
# Avviare l'app
source .venv/bin/activate
python -m src.app

# Installare avvio automatico
cp scripts/com.voicetoclaude.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.voicetoclaude.plist

# Disinstallare avvio automatico
launchctl unload ~/Library/LaunchAgents/com.voicetoclaude.plist
rm ~/Library/LaunchAgents/com.voicetoclaude.plist
```

## Hotkey

- **Cmd+Shift+V**: Toggle registrazione

## Paths

- Modello: `~/.local/share/whisper-cpp/models/ggml-large-v3.bin`
- Logs: `~/Library/Logs/voice-to-claude/`
- Trascrizioni: `~/Documents/voice-transcripts/`

## Permessi Richiesti

1. **Accessibilità**: System Preferences > Privacy & Security > Accessibility
2. **Microfono**: System Preferences > Privacy & Security > Microphone

## Troubleshooting

| Problema | Soluzione |
|----------|-----------|
| Hotkey non funziona | Verificare permesso Accessibilità |
| Nessun audio | Verificare permesso Microfono |
| Trascrizione lenta | Modello large-v3 richiede ~30s per audio lungo |
