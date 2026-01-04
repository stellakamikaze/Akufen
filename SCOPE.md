# Voice-to-Claude - Scope Document

## Overview
Applicazione menubar per macOS che permette di dettare testo vocalmente e incollarlo automaticamente in qualsiasi applicazione. Usa Whisper.cpp per trascrizione locale (offline), supporta italiano e inglese, con feedback audio/visivo.

## Phase 1: Foundation

### 1.1 Setup Progetto
- [ ] Task 1.1.1: Creare struttura directory progetto
- [ ] Task 1.1.2: Creare virtual environment Python
- [ ] Task 1.1.3: Creare requirements.txt con dipendenze
- [ ] Task 1.1.4: Creare CLAUDE.md progetto

### 1.2 Installazione Whisper.cpp
- [ ] Task 1.2.1: Installare whisper.cpp via Homebrew
- [ ] Task 1.2.2: Scaricare modello large-v3
- [ ] Task 1.2.3: Testare trascrizione da CLI
- [ ] Task 1.2.4: Documentare path e comandi

### 1.3 Audio Recording
- [ ] Task 1.3.1: Implementare registrazione audio con sounddevice
- [ ] Task 1.3.2: Salvare audio in formato WAV (16kHz, mono)
- [ ] Task 1.3.3: Testare qualità registrazione
- [ ] Task 1.3.4: Gestire selezione microfono (default system)

## Phase 2: Core Features

### 2.1 Menubar App
- [ ] Task 2.1.1: Creare app menubar con rumps
- [ ] Task 2.1.2: Icona stato: idle (grigia), recording (rossa)
- [ ] Task 2.1.3: Menu dropdown: Quit, About, Status
- [ ] Task 2.1.4: Mostrare stato corrente nel menu

### 2.2 Hotkey Globale
- [ ] Task 2.2.1: Registrare hotkey Cmd+Shift+V con pynput
- [ ] Task 2.2.2: Toggle start/stop registrazione
- [ ] Task 2.2.3: Gestire conflitti hotkey esistenti
- [ ] Task 2.2.4: Verificare permessi Accessibilità

### 2.3 Trascrizione
- [ ] Task 2.3.1: Chiamare whisper.cpp su file audio
- [ ] Task 2.3.2: Parsare output testo
- [ ] Task 2.3.3: Auto-detect lingua (IT/EN)
- [ ] Task 2.3.4: Gestire timeout/errori trascrizione

### 2.4 Output & Paste
- [ ] Task 2.4.1: Copiare testo in clipboard (pyperclip)
- [ ] Task 2.4.2: Simulare Cmd+V per paste automatico
- [ ] Task 2.4.3: Ritardo configurabile prima del paste
- [ ] Task 2.4.4: Notifica successo trascrizione

### 2.5 Audio Feedback
- [ ] Task 2.5.1: Beep inizio registrazione
- [ ] Task 2.5.2: Beep fine registrazione (diverso)
- [ ] Task 2.5.3: Suono errore
- [ ] Task 2.5.4: Usare suoni di sistema macOS

## Phase 3: Polish & Operations

### 3.1 Logging & Debug
- [ ] Task 3.1.1: Setup logging con rotazione file
- [ ] Task 3.1.2: Log path: ~/Library/Logs/voice-to-claude/
- [ ] Task 3.1.3: Livelli: DEBUG, INFO, ERROR
- [ ] Task 3.1.4: Log eventi: start, stop, transcription, errors

### 3.2 Notifiche Native
- [ ] Task 3.2.1: Notifica errore trascrizione
- [ ] Task 3.2.2: Notifica permessi mancanti
- [ ] Task 3.2.3: Usare pync o osascript per notifiche
- [ ] Task 3.2.4: Notifica primo avvio (setup completato)

### 3.3 Cronologia Trascrizioni
- [ ] Task 3.3.1: Creare directory ~/Documents/voice-transcripts/
- [ ] Task 3.3.2: Salvare ogni trascrizione con timestamp
- [ ] Task 3.3.3: Formato: YYYY-MM-DD_HH-MM-SS.txt
- [ ] Task 3.3.4: Includere metadati (durata, lingua)

### 3.4 Cleanup & Sicurezza
- [ ] Task 3.4.1: Cancellare file audio dopo trascrizione
- [ ] Task 3.4.2: Gestire file orfani in /tmp/
- [ ] Task 3.4.3: Non loggare contenuto trascrizioni (privacy)

### 3.5 Avvio Automatico
- [ ] Task 3.5.1: Creare LaunchAgent plist
- [ ] Task 3.5.2: Installare in ~/Library/LaunchAgents/
- [ ] Task 3.5.3: Comando install/uninstall nel menu
- [ ] Task 3.5.4: Testare avvio al login

## Phase 4: Release

### 4.1 Documentazione
- [ ] Task 4.1.1: README.md con istruzioni installazione
- [ ] Task 4.1.2: Documentare requisiti (permessi, Homebrew)
- [ ] Task 4.1.3: Screenshot/GIF demo
- [ ] Task 4.1.4: Troubleshooting comune

### 4.2 Packaging
- [ ] Task 4.2.1: Script setup.sh per installazione completa
- [ ] Task 4.2.2: Testare su macchina pulita
- [ ] Task 4.2.3: Creare repo GitHub
- [ ] Task 4.2.4: Licenza MIT

## Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Linguaggio | Python 3.10+ | Ecosistema ricco, velocità sviluppo |
| GUI | rumps | Menubar nativa macOS, leggera |
| Speech-to-text | whisper.cpp | Locale, Metal GPU, accurato |
| Modello | large-v3 | Migliore accuratezza OSS |
| Audio | sounddevice | Cross-platform, semplice API |
| Hotkey | pynput | Hotkey globali, cross-platform |
| Clipboard | pyperclip | Semplice, affidabile |
| Notifiche | pync | Wrapper per terminal-notifier |

## File Structure

```
voice-to-claude/
├── src/
│   ├── __init__.py
│   ├── app.py           # Entry point, menubar app
│   ├── recorder.py      # Audio recording
│   ├── transcriber.py   # Whisper.cpp wrapper
│   ├── hotkey.py        # Global hotkey handler
│   ├── clipboard.py     # Clipboard & paste
│   ├── notifier.py      # macOS notifications
│   └── config.py        # Configuration constants
├── resources/
│   ├── icon_idle.png    # Menubar icon (idle)
│   ├── icon_recording.png
│   └── sounds/          # Beep sounds (optional)
├── scripts/
│   ├── setup.sh         # Installation script
│   └── com.voicetoclaude.plist  # LaunchAgent
├── tests/
│   └── test_transcriber.py
├── requirements.txt
├── CLAUDE.md
├── SCOPE.md
├── README.md
└── LICENSE
```

## Success Criteria

- [ ] Hotkey Cmd+Shift+V attiva/ferma registrazione
- [ ] Trascrizione accurata italiano e inglese
- [ ] Paste automatico funziona in Terminal, iTerm2, browser
- [ ] Feedback audio udibile
- [ ] Icona menubar cambia stato
- [ ] Avvio automatico al login funzionante
- [ ] Zero file audio residui dopo trascrizione
- [ ] Log errori consultabili per debug

## Out of Scope (v2)

- Selezione lingua manuale da menu
- Hotkey personalizzabile da UI
- UI per consultare cronologia trascrizioni
- Comandi vocali ("cancella ultimo", "invia")
- Integrazione diretta con Claude Code API
- Supporto Windows/Linux
- App bundle .app firmata

## Dependencies

```
rumps>=0.4.0
sounddevice>=0.4.6
numpy>=1.24.0
pynput>=1.7.6
pyperclip>=1.8.2
pync>=2.0.3
```

## External Requirements

- macOS 11+ (Big Sur o successivo)
- Homebrew installato
- whisper.cpp: `brew install whisper-cpp`
- Modello: `whisper-cpp-download-ggml-model large-v3`
- Permessi: Accessibilità + Microfono
