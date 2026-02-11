# 🎙️ Voice Wake Linux

A voice assistant for Linux that brings hands-free voice control to your desktop, Raspberry Pi, or any Linux system.

**Created and developed by JARVIS, an OpenClaw AI assistant**

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)

## ✨ Overview

Voice Wake Linux is an open-source voice assistant that combines:
- **Wake Word Detection** — OpenWakeWord for efficient, low-latency recognition
- **Speech-to-Text** — Google Speech API for accurate transcription
- **AI Integration** — Seamless OpenClaw connection for intelligent responses
- **Text-to-Speech** — Speaks responses back to you
- **Multi-Turn Conversations** — Context-aware, maintains conversation state

### 🤖 About JARVIS

JARVIS is an AI assistant running on **OpenClaw** — an AI platform that enables AI agents to perform tasks, write code, and interact with systems. This project was conceived, designed, and implemented by JARVIS.

OpenClaw provides the AI intelligence that powers JARVIS, allowing it to understand context, execute commands, and generate natural language responses through voice interaction.

Say **"Hey Jarvis"** to activate, speak your command, and get a spoken response.

## 🚀 Key Features

- ✅ Wake word detection ("Hey Jarvis")
- ✅ Accurate speech recognition
- ✅ AI-powered responses
- ✅ Text-to-speech output
- ✅ Multi-turn conversations with context
- ✅ 10-second command recording
- ✅ Audio confirmation on wake word
- ✅ Cross-platform (Raspberry Pi, Ubuntu, Fedora, Arch, etc.)
- ✅ Lightweight and open source

## 📋 Requirements

- Linux OS
- Python 3.8+
- Microphone and speakers/headphones
- Internet connection

### Dependencies
- PortAudio (audio I/O)
- espeak/espeak-ng (TTS)
- ALSA utilities (audio playback)
- ffmpeg (MP3 support)

## 🛠️ Installation

### Quick Install (Ubuntu/Debian)

```bash
git clone https://github.com/kaushikshiv/voice-wake-linux.git
cd voice-wake-linux
chmod +x install.sh
./install.sh
```

### Manual Install

```bash
# System dependencies
sudo apt-get install -y python3 python3-pip python3-venv portaudio19-dev \
    python3-dev espeak espeak-data alsa-utils ffmpeg libportaudio2

# Virtual environment
python3 -m venv venv
source venv/bin/activate

# Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Make scripts executable
chmod +x scripts/voice_wake.py scripts/voice_wake_wrapper.sh
```

### Other Distros

**Fedora:**
```bash
sudo dnf install -y python3 python3-pip portaudio-devel python3-devel \
    espeak espeak-ng alsa-utils ffmpeg portaudio
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

**Arch:**
```bash
sudo pacman -S --noconfirm python python-pip portaudio espeak-ng alsa-utils ffmpeg
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

## ⚙️ Configuration

Edit `config.py`:

```python
class Config:
    # Wake word
    WAKE_WORD = 'hey_jarvis'  # Options: alexa, hey_mycroft, hey_jarvis
    DETECTION_THRESHOLD = 0.3  # 0.0-1.0, lower = more sensitive

    # OpenClaw
    OPENCLAW_CLI = 'openclaw'
    SESSION_ID = 'voice:wake:main'

    # Audio
    AUDIO_DEVICE_INDEX = None  # None = default mic
    SAMPLE_RATE = 16000
    CHUNK_SIZE = 1280
    CHANNELS = 1

    # Recording
    RECORDING_TIMEOUT = 10  # seconds
    PHRASE_TIMEOUT = 3      # seconds

    # TTS
    ENABLE_TTS = True
    AUDIO_PLAYER = 'aplay'  # Options: aplay, paplay, ffplay
    MP3_PLAYER = 'ffplay'
```

### Find Your Audio Device

```bash
# List microphones
arecord -l

# List speakers
aplay -l
```

Set `AUDIO_DEVICE_INDEX` in config.py to the device number.

## 🎯 Usage

### Run Manually

```bash
source venv/bin/activate
./scripts/voice_wake.py
```

### Example Session

1. Say **"Hey Jarvis"** → hear beep
2. Speak your command (e.g., "What time is it?")
3. Listen to the response
4. Say "Hey Jarvis" again for more commands

### Example Commands

- "What's the weather today?"
- "What's the capital of France?" (then "And what's the population?")
- "Tell me a joke"
- "What's 25 times 17?"

## 🔄 Systemd Service

### Setup

```bash
mkdir -p ~/.config/systemd/user
cp voice-wake.service ~/.config/systemd/user/
nano ~/.config/systemd/user/voice-wake.service  # Update paths
```

Edit these lines:
```ini
WorkingDirectory=/home/YOUR_USERNAME/voice-wake-linux/scripts
ExecStart=/home/YOUR_USERNAME/voice-wake-linux/scripts/voice_wake_wrapper.sh
Environment=HOME=/home/YOUR_USERNAME
```

### Start Service

```bash
systemctl --user daemon-reload
systemctl --user enable voice-wake.service
systemctl --user start voice-wake.service
systemctl --user status voice-wake.service
```

### Management

```bash
systemctl --user {start|stop|restart} voice-wake.service
journalctl --user -u voice-wake.service -f
tail -f voice_wake.log
```

## 🔍 Troubleshooting

| Issue | Solution |
|-------|----------|
| Wake word not detected | Lower `DETECTION_THRESHOLD` (try 0.2 or 0.15), check mic with `alsamixer` |
| No audio output | Check `aplay` is installed, test with `aplay /usr/share/sounds/alsa/Front_Center.wav`, verify `ENABLE_TTS = True` |
| Speech recognition fails | Check internet connection, verify mic works with `arecord -f cd test.wav` |
| Service won't start | Check status: `systemctl --user status voice-wake.service`, view logs: `journalctl --user -u voice-wake.service -n 50` |
| ImportError | Activate venv: `source venv/bin/activate`, reinstall: `pip install -r requirements.txt` |
| High CPU | Increase `CHUNK_SIZE` (try 2560), reduce `SAMPLE_RATE` (try 8000), lower `DETECTION_THRESHOLD` |

## 📚 Project Structure

```
voice-wake-linux/
├── README.md
├── install.sh
├── requirements.txt
├── voice-wake.service
├── config.py
├── voice_wake.log
├── scripts/
│   ├── voice_wake.py
│   └── voice_wake_wrapper.sh
├── docs/
│   ├── architecture.md
│   └── api.md
└── venv/
```

## 🤝 Contributing

Contributions welcome! Report bugs, suggest features, submit pull requests, improve documentation, or share your use cases.

## 📄 License

MIT License — see LICENSE file.

## 🙏 Acknowledgments

- [OpenWakeWord](https://github.com/dscripka/openWakeWord) — Wake word detection
- [SpeechRecognition](https://github.com/Uberi/speech_recognition) — Speech-to-text
- [OpenClaw](https://openclaw.ai) — AI integration platform
- [espeak](https://espeak.sourceforge.net/) — TTS engine

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/kaushikshiv/voice-wake-linux/issues)
- **Discussions**: [GitHub Discussions](https://github.com/kaushikshiv/voice-wake-linux/discussions)
- **Email**: kaushik.sivashankar@gmail.com

---

**Created and developed by JARVIS, an OpenClaw AI assistant**

Built on **OpenClaw** — an AI platform that enables AI agents to create and interact with systems.

*Maintained by Kaushik Sivashankar*
