# 🎙️ Voice Wake Linux

A groundbreaking voice assistant integration for Linux that brings hands-free voice control to your desktop, Raspberry Pi, or any Linux system.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)

## ✨ What Makes It Unique?

Voice Wake Linux is a **first-of-its-kind** open-source project that combines:

- **Wake Word Detection**: Uses OpenWakeWord for efficient, low-latency wake word recognition
- **Speech-to-Text**: Leverages Google's free Web Speech API for accurate transcription
- **AI Integration**: Seamlessly connects to OpenClaw for intelligent responses
- **Text-to-Speech**: Speaks responses back to you using TTS
- **Multi-Turn Conversations**: Maintains context across multiple voice commands
- **Session Continuity**: All voice commands go to the same session for coherent conversations

Unlike other voice assistants that require cloud services or expensive hardware, Voice Wake Linux runs entirely on your machine with minimal dependencies.

## 🚀 Features

### Core Features
- ✅ **Wake Word Detection** - Say "Hey Jarvis" to activate
- ✅ **Speech Recognition** - Accurate transcription using Google Speech API
- ✅ **AI Integration** - Connects to OpenClaw for intelligent responses
- ✅ **Text-to-Speech** - Speaks responses aloud
- ✅ **Multi-Turn Conversations** - Context-aware voice interactions
- ✅ **Session Continuity** - Maintains conversation state
- ✅ **Audio Feedback** - Beep confirmation when wake word detected
- ✅ **10-Second Recording** - Consistent recording window for commands
- ✅ **Cross-Platform** - Works on Raspberry Pi, Ubuntu, Fedora, Arch, and more
- ✅ **Lightweight** - Minimal resource usage
- ✅ **Open Source** - Fully customizable and extensible

### Advanced Features
- 🎯 **Configurable Wake Words** - Choose from multiple pre-trained models
- 🔧 **Adjustable Sensitivity** - Fine-tune detection threshold
- 📊 **Comprehensive Logging** - Detailed logs for debugging
- 🔄 **Auto-Restart** - Systemd service with auto-recovery
- 🎵 **MP3 Response Playback** - Supports audio responses
- 🔊 **Multiple Audio Players** - Works with aplay, paplay, ffplay, etc.

## 📋 Requirements

### System Requirements
- Linux operating system (Ubuntu, Debian, Fedora, Arch, Raspberry Pi OS, etc.)
- Python 3.8 or higher
- Microphone
- Speakers or headphones
- Internet connection (for speech recognition and AI responses)

### Dependencies
- PortAudio (for audio I/O)
- espeak or espeak-ng (for text-to-speech)
- ALSA utilities (for audio playback)
- ffmpeg (for MP3 support)

## 🛠️ Installation

### Quick Install (Ubuntu/Debian)

```bash
# Clone the repository
git clone https://github.com/kaushikshiv/voice-wake-linux.git
cd voice-wake-linux

# Run the installation script
chmod +x install.sh
./install.sh
```

### Manual Install

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv \
    portaudio19-dev python3-dev espeak espeak-data \
    alsa-utils ffmpeg libportaudio2

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Make scripts executable
chmod +x scripts/voice_wake.py
chmod +x scripts/voice_wake_wrapper.sh
```

### Fedora Install

```bash
# Install system dependencies
sudo dnf install -y python3 python3-pip portaudio-devel \
    python3-devel espeak espeak-ng alsa-utils ffmpeg portaudio

# Create virtual environment and install Python dependencies
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Arch Linux Install

```bash
# Install system dependencies
sudo pacman -S --noconfirm python python-pip portaudio \
    espeak-ng alsa-utils ffmpeg

# Create virtual environment and install Python dependencies
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## ⚙️ Configuration

### Basic Configuration

Edit `config.py` to customize settings:

```python
class Config:
    # Wake word settings
    WAKE_WORD = 'hey_jarvis'  # Available: alexa, hey_mycroft, hey_jarvis
    DETECTION_THRESHOLD = 0.3  # Sensitivity (0.0-1.0)

    # OpenClaw integration
    OPENCLAW_CLI = 'openclaw'  # Path to openclaw CLI
    SESSION_ID = 'voice:wake:main'  # Session key for continuity

    # Audio settings
    AUDIO_DEVICE_INDEX = None  # None for default mic, or set device number
    SAMPLE_RATE = 16000
    CHUNK_SIZE = 1280
    CHANNELS = 1

    # Recording settings
    RECORDING_TIMEOUT = 10  # seconds
    PHRASE_TIMEOUT = 3      # seconds

    # TTS settings
    ENABLE_TTS = True  # Enable/disable spoken responses
    AUDIO_PLAYER = 'aplay'  # Audio player command
    MP3_PLAYER = 'ffplay'  # MP3 player command
```

### Finding Your Audio Device

List available audio devices:

```bash
# List playback devices
aplay -l

# List capture devices (microphones)
arecord -l

# Or run the script and check the logs
./scripts/voice_wake.py
```

Set `AUDIO_DEVICE_INDEX` in config.py to the appropriate device number.

### Changing the Wake Word

Available pre-trained wake words:
- `alexa`
- `hey_mycroft`
- `hey_jarvis` (default)

Change the `WAKE_WORD` setting in `config.py`.

## 🎯 Usage

### Running Manually

```bash
# Activate virtual environment
source venv/bin/activate

# Run the voice wake service
./scripts/voice_wake.py
```

### Usage Example

1. Start the service
2. Say **"Hey Jarvis"**
3. Wait for the beep
4. Speak your command (e.g., "What time is it?")
5. Listen to the response
6. Say "Hey Jarvis" again for more commands

### Example Commands

```bash
# Weather
"Hey Jarvis" → "What's the weather like today?"

# Time
"Hey Jarvis" → "What time is it?"

# Information
"Hey Jarvis" → "Tell me a joke"

# Math
"Hey Jarvis" → "What's 25 times 17?"

# Multi-turn conversations
"Hey Jarvis" → "What's the capital of France?"
"Hey Jarvis" → "And what's the population?"
```

## 🔄 Installing as a Systemd Service

### Setup

```bash
# Copy the service file
mkdir -p ~/.config/systemd/user
cp voice-wake.service ~/.config/systemd/user/

# Edit the service file to update paths
nano ~/.config/systemd/user/voice-wake.service
```

Update these lines in the service file:
```ini
WorkingDirectory=/home/YOUR_USERNAME/voice-wake-linux/scripts
ExecStart=/home/YOUR_USERNAME/voice-wake-linux/scripts/voice_wake_wrapper.sh
Environment=HOME=/home/YOUR_USERNAME
```

### Enable and Start

```bash
# Reload systemd
systemctl --user daemon-reload

# Enable the service (auto-start on login)
systemctl --user enable voice-wake.service

# Start the service
systemctl --user start voice-wake.service

# Check status
systemctl --user status voice-wake.service
```

### Service Management

```bash
# Start service
systemctl --user start voice-wake.service

# Stop service
systemctl --user stop voice-wake.service

# Restart service
systemctl --user restart voice-wake.service

# View logs
journalctl --user -u voice-wake.service -f

# View log file
tail -f voice_wake.log
```

## 🔍 Troubleshooting

### Wake Word Not Detected

**Problem**: Wake word is not being detected.

**Solutions**:
1. Lower the `DETECTION_THRESHOLD` in config.py (try 0.2 or 0.15)
2. Check microphone levels with `alsamixer`
3. Verify your microphone is working: `arecord -f cd test.wav && aplay test.wav`
4. Try a different audio device by setting `AUDIO_DEVICE_INDEX`
5. Ensure you're speaking clearly and at a moderate volume

### No Audio Output

**Problem**: TTS responses are not playing.

**Solutions**:
1. Check if audio player is installed: `which aplay` or `which paplay`
2. Test audio player: `aplay /usr/share/sounds/alsa/Front_Center.wav`
3. Check speaker volume with `alsamixer`
4. Verify `ENABLE_TTS = True` in config.py
5. Check logs for errors: `tail -f voice_wake.log`

### Speech Recognition Fails

**Problem**: Commands are not being transcribed.

**Solutions**:
1. Check internet connection (required for Google Speech API)
2. Verify microphone is recording: `arecord -f cd test.wav`
3. Try speaking more clearly and closer to the microphone
4. Check for errors in logs: `tail -f voice_wake.log`

### Service Won't Start

**Problem**: Systemd service fails to start.

**Solutions**:
1. Check service status: `systemctl --user status voice-wake.service`
2. View service logs: `journalctl --user -u voice-wake.service -n 50`
3. Verify paths in voice-wake.service are correct
4. Ensure virtual environment is activated in wrapper script
5. Check file permissions: `ls -la scripts/`

### ImportError or Module Not Found

**Problem**: Python modules are missing.

**Solutions**:
1. Activate virtual environment: `source venv/bin/activate`
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check Python version: `python3 --version` (must be 3.8+)
4. Verify pip is up to date: `pip install --upgrade pip`

### High CPU Usage

**Problem**: Service uses too much CPU.

**Solutions**:
1. Increase `CHUNK_SIZE` in config.py (try 2560 or 5120)
2. Reduce `SAMPLE_RATE` (try 8000 instead of 16000)
3. Lower `DETECTION_THRESHOLD` to reduce false positives
4. Check if other audio applications are running

## 📚 Advanced Configuration

### Custom Wake Words

You can train custom wake words using OpenWakeWord's tools:

```bash
# Install OpenWakeWord training tools
pip install openwakeword

# Follow the training guide at:
# https://github.com/dscripka/openWakeWord
```

### Multiple Audio Devices

If you have multiple microphones, specify the device index:

```python
# List devices first (check logs when running the script)
# Then set the index in config.py
AUDIO_DEVICE_INDEX = 1  # Use second microphone
```

### Integration with Other AI Services

The service can be easily modified to work with other AI services:

1. Modify the `send_to_openclaw()` method in `scripts/voice_wake.py`
2. Replace the OpenClaw CLI call with your preferred API
3. Ensure the response format matches the expected structure

### Custom TTS Engines

Replace espeak with other TTS engines:

```python
# In scripts/voice_wake.py, modify text_to_speech() method
# Examples: pico2wave, festival, marytts, etc.
```

## 📖 Project Structure

```
voice-wake-linux/
├── README.md                 # This file
├── install.sh                # Installation script
├── requirements.txt          # Python dependencies
├── voice-wake.service        # Systemd service file
├── config.py                 # Configuration file (created after install)
├── voice_wake.log            # Log file (created at runtime)
├── scripts/
│   ├── voice_wake.py         # Main voice wake service
│   └── voice_wake_wrapper.sh # Service wrapper script
├── docs/
│   ├── architecture.md       # System architecture documentation
│   └── api.md                # API documentation
├── examples/
│   └── custom_integration.py # Example custom integrations
└── venv/                     # Virtual environment (created after install)
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report bugs** - Open an issue with detailed information
2. **Suggest features** - Share ideas for improvements
3. **Submit pull requests** - Fix bugs or add new features
4. **Improve documentation** - Help make the project more accessible
5. **Share your use cases** - Tell us how you're using Voice Wake Linux

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [OpenWakeWord](https://github.com/dscripka/openWakeWord) - Wake word detection
- [SpeechRecognition](https://github.com/Uberi/speech_recognition) - Speech-to-text
- [OpenClaw](https://openclaw.ai) - AI integration platform
- [espeak](https://espeak.sourceforge.net/) - Text-to-speech engine

## 🔗 Links

- [OpenWakeWord Documentation](https://github.com/dscripka/openWakeWord)
- [SpeechRecognition Library](https://github.com/Uberi/speech_recognition)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/kaushikshiv/voice-wake-linux/issues)
- **Discussions**: [GitHub Discussions](https://github.com/kaushikshiv/voice-wake-linux/discussions)
- **Email**: kaushik.sivashankar@gmail.com

## 🌟 Star History

If you find this project useful, please consider giving it a star on GitHub!

---

**Made with ❤️ by Kaushik Sivashankar**

*Bringing voice control to Linux, one wake word at a time.*
