# Changelog

All notable changes to Voice Wake Linux will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-11

### Added
- Initial release of Voice Wake Linux
- Wake word detection using OpenWakeWord ("Hey Jarvis")
- Speech recognition using Google Web Speech API
- OpenClaw AI integration for intelligent responses
- Text-to-speech with OpenClaw TTS and espeak fallback
- Session continuity for multi-turn conversations
- Audio feedback beep when wake word detected
- Fixed 10-second recording window for commands
- Comprehensive configuration system
- Systemd service support for background operation
- Cross-platform Linux support (Ubuntu, Debian, Fedora, Arch, Raspberry Pi)
- Detailed logging and error handling
- Installation script for easy setup
- Comprehensive documentation

### Features
- **Wake Word Detection**: Detects "Hey Jarvis" with configurable sensitivity
- **Speech-to-Text**: High-accuracy transcription of voice commands
- **AI Integration**: Seamless connection to OpenClaw for intelligent responses
- **Text-to-Speech**: Speaks responses aloud with multiple TTS engines
- **Session Management**: Maintains context across multiple voice interactions
- **Audio Feedback**: Pleasant beep sound confirms wake word detection
- **Multi-Platform**: Works on various Linux distributions and Raspberry Pi
- **Service Integration**: Runs as systemd service with auto-restart
- **Configuration**: Highly customizable through config files
- **Error Recovery**: Graceful handling of errors with fallback mechanisms

### Documentation
- Comprehensive README with installation and usage instructions
- System architecture documentation
- Configuration examples and explanations
- Troubleshooting guide for common issues
- Installation script for automated setup

### Supported Platforms
- Ubuntu 18.04+
- Debian 10+
- Fedora 32+
- Arch Linux
- Raspberry Pi OS
- Other Linux distributions with minor modifications

### Dependencies
- Python 3.8+
- OpenWakeWord
- SpeechRecognition
- PyAudio
- NumPy
- espeak or espeak-ng
- ALSA utilities
- ffmpeg (for MP3 support)

### Known Issues
- Requires internet connection for speech recognition
- Google Speech API has daily rate limits (free tier)
- Some audio devices may require manual configuration
- Wake word sensitivity may need adjustment for different environments

### Future Enhancements
- Additional pre-trained wake words
- Custom wake word training support
- Multi-language support
- Web interface for configuration
- Mobile app integration
- Voice recognition for multi-user support
- Improved offline capabilities

## [Unreleased]

### Planned Features
- [ ] Additional wake words (custom training)
- [ ] Multi-language speech recognition
- [ ] Web-based configuration interface
- [ ] Mobile app for remote control
- [ ] Voice profiles for multiple users
- [ ] Offline speech recognition option
- [ ] Plugin system for extensibility
- [ ] Enhanced audio processing
- [ ] Advanced conversation management
- [ ] Integration with home automation systems

---

For more details about each release, see the [GitHub releases page](https://github.com/kaushikshiv/voice-wake-linux/releases).