#!/bin/bash
# Installation script for Voice Wake Linux

set -e

echo "=========================================="
echo "Voice Wake Linux - Installation Script"
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "Please do not run this script as root. Use a regular user account."
    exit 1
fi

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "Cannot detect OS. Exiting."
    exit 1
fi

echo "Detected OS: $OS"
echo ""

# Update package lists
echo "Updating package lists..."
if command -v apt-get &> /dev/null; then
    sudo apt-get update
elif command -v dnf &> /dev/null; then
    sudo dnf check-update || true
elif command -v pacman &> /dev/null; then
    sudo pacman -Sy
else
    echo "Warning: Could not update package lists. Unknown package manager."
fi
echo ""

# Install system dependencies
echo "Installing system dependencies..."
if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
    sudo apt-get install -y \
        python3 \
        python3-pip \
        python3-venv \
        portaudio19-dev \
        python3-dev \
        espeak \
        espeak-data \
        alsa-utils \
        ffmpeg \
        libportaudio2
elif [ "$OS" = "fedora" ]; then
    sudo dnf install -y \
        python3 \
        python3-pip \
        portaudio-devel \
        python3-devel \
        espeak \
        espeak-ng \
        alsa-utils \
        ffmpeg \
        portaudio
elif [ "$OS" = "arch" ] || [ "$OS" = "manjaro" ]; then
    sudo pacman -S --noconfirm \
        python \
        python-pip \
        portaudio \
        espeak-ng \
        alsa-utils \
        ffmpeg
else
    echo "Warning: Your OS is not explicitly supported. Please install the following packages manually:"
    echo "  - Python 3 and pip"
    echo "  - PortAudio development libraries"
    echo "  - espeak or espeak-ng"
    echo "  - ALSA utilities"
    echo "  - ffmpeg"
fi
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "Python version: $(python3 --version)"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
echo "✅ Virtual environment created"
echo ""

# Activate virtual environment and install Python dependencies
echo "Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Python dependencies installed"
echo ""

# Make scripts executable
echo "Making scripts executable..."
chmod +x scripts/voice_wake.py
chmod +x scripts/voice_wake_wrapper.sh
echo "✅ Scripts made executable"
echo ""

# Create configuration file
echo "Creating configuration file..."
if [ ! -f "config.py" ]; then
    cat > config.py << 'EOF'
# Voice Wake Linux Configuration
# Copy this file and customize for your setup

class Config:
    # OpenWakeWord settings
    WAKE_WORD = 'hey_jarvis'  # Available: alexa, hey_mycroft, hey_jarvis
    DETECTION_THRESHOLD = 0.3  # Sensitivity (0.0-1.0), lower = more sensitive

    # OpenClaw settings
    # Set to 'openclaw' if installed globally, or provide full path
    OPENCLAW_CLI = 'openclaw'
    SESSION_ID = 'voice:wake:main'  # Session key for multi-turn conversations

    # Audio settings
    AUDIO_DEVICE_INDEX = None  # None for default, or set to device number
    SAMPLE_RATE = 16000
    CHUNK_SIZE = 1280  # 80ms chunks
    CHANNELS = 1

    # Recording settings
    RECORDING_TIMEOUT = 10  # seconds to record after wake word
    PHRASE_TIMEOUT = 3      # seconds of silence to stop recording

    # TTS settings
    ENABLE_TTS = True  # Set to False to disable spoken responses
    AUDIO_PLAYER = 'aplay'  # Audio player (aplay, paplay, etc.)
    MP3_PLAYER = 'ffplay'  # MP3 player (ffplay, mpg123, etc.)

    # Logging
    LOG_FILE = 'voice_wake.log'  # Log file path
    LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
EOF
    echo "✅ Configuration file created (config.py)"
else
    echo "ℹ️  Configuration file already exists (config.py)"
fi
echo ""

echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Configure the system:"
echo "   - Edit config.py to customize settings"
echo "   - Update OPENCLAW_CLI path if needed"
echo "   - Adjust AUDIO_DEVICE_INDEX if you have multiple microphones"
echo ""
echo "2. Test the service:"
echo "   - Run: ./scripts/voice_wake.py"
echo "   - Say 'Hey Jarvis' to test wake word detection"
echo ""
echo "3. Install as a systemd service (optional):"
echo "   - Edit voice-wake.service to update paths"
echo "   - Copy to ~/.config/systemd/user/"
echo "   - Run: systemctl --user enable voice-wake.service"
echo "   - Run: systemctl --user start voice-wake.service"
echo ""
echo "For more information, see README.md"
echo ""
