#!/bin/bash
# Voice Wake Wrapper Script with TTS
# Activates the virtual environment and runs the voice wake service

# Set up logging
exec 1> >(logger -t voice-wake-wrapper -p local0.info)
exec 2> >(logger -t voice-wake-wrapper -p local0.error)

echo "Starting Voice Wake Service with TTS..."

# Activate virtual environment - UPDATE THIS PATH
# source /path/to/your/venv/bin/activate

# Set working directory
cd "$(dirname "$0")"

# Run the voice wake service with TTS
python3 voice_wake.py

# Log exit
echo "Voice Wake Service exited with code $?"
