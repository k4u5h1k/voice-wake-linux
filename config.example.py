# Voice Wake Linux Configuration
# This is an example configuration file
# Copy this to config.py and customize for your setup

class Config:
    """
    Voice Wake Linux Configuration
    Adjust these settings to customize behavior
    """

    # ═══════════════════════════════════════════════════════════
    # WAKE WORD SETTINGS
    # ═══════════════════════════════════════════════════════════

    # Available wake words (pre-trained models):
    # - 'alexa': Trained on "Alexa" wake word
    # - 'hey_mycroft': Trained on "Hey Mycroft" wake word
    # - 'hey_jarvis': Trained on "Hey Jarvis" wake word (default)
    WAKE_WORD = 'hey_jarvis'

    # Detection sensitivity (0.0 to 1.0)
    # Lower values = more sensitive (may cause false positives)
    # Higher values = less sensitive (may miss wake words)
    # Recommended: 0.3 to 0.5
    DETECTION_THRESHOLD = 0.3

    # Cooldown period between wake word detections (seconds)
    # Prevents rapid re-triggering of the same wake word
    WAKE_WORD_COOLDOWN = 3

    # ═══════════════════════════════════════════════════════════
    # OPENCLAW AI INTEGRATION
    # ═══════════════════════════════════════════════════════════

    # Path to OpenClaw CLI
    # Use 'openclaw' if installed in PATH, or provide full path
    # Examples:
    #   OPENCLAW_CLI = 'openclaw'  # If in PATH
    #   OPENCLAW_CLI = '/usr/local/bin/openclaw'  # Full path
    #   OPENCLAW_CLI = '/home/user/.npm-global/bin/openclaw'  # NPM global
    OPENCLAW_CLI = 'openclaw'

    # Session key for conversation continuity
    # All voice commands with the same session key maintain context
    # Use different keys for different conversation contexts
    # Example: 'voice:wake:main', 'voice:wake:work', 'voice:wake:personal'
    SESSION_ID = 'voice:wake:main'

    # ═══════════════════════════════════════════════════════════
    # AUDIO SETTINGS
    # ═══════════════════════════════════════════════════════════

    # Audio device index for microphone
    # None = use default microphone
    # To find your microphone index:
    # 1. Run the script and check the logs for "Available audio devices"
    # 2. Or use: arecord -l
    # 3. Set the number corresponding to your microphone
    AUDIO_DEVICE_INDEX = None

    # Audio sample rate (Hz)
    # 16000 is optimal for speech recognition
    # 8000 can be used for lower CPU usage but with reduced accuracy
    SAMPLE_RATE = 16000

    # Audio chunk size (samples per chunk)
    # 1280 = 80ms chunks (recommended)
    # Larger values = higher CPU usage but slightly better accuracy
    # Smaller values = lower CPU usage but may reduce accuracy
    CHUNK_SIZE = 1280

    # Audio channels
    # 1 = mono (recommended for voice)
    # 2 = stereo
    CHANNELS = 1

    # ═══════════════════════════════════════════════════════════
    # RECORDING SETTINGS
    # ═══════════════════════════════════════════════════════════

    # Recording duration after wake word (seconds)
    # This is the fixed time window for speaking your command
    # Recommended: 10 seconds
    RECORDING_TIMEOUT = 10

    # Phrase timeout (not used in current implementation)
    # Kept for future use with variable-length recording
    PHRASE_TIMEOUT = 3

    # ═══════════════════════════════════════════════════════════
    # TEXT-TO-SPEECH (TTS) SETTINGS
    # ═══════════════════════════════════════════════════════════

    # Enable/disable spoken responses
    # True = Speak responses aloud
    # False = Log responses only (no audio output)
    ENABLE_TTS = True

    # Audio player for WAV files
    # Options:
    #   'aplay' - ALSA player (most common)
    #   'paplay' - PulseAudio player
    #   'play' - SoX player
    AUDIO_PLAYER = 'aplay'

    # MP3 player for MEDIA: responses
    # Options:
    #   'ffplay' - FFmpeg player (recommended)
    #   'mpg123' - Lightweight MP3 player
    #   'mpg321' - Alternative MP3 player
    MP3_PLAYER = 'ffplay'

    # TTS engine priority
    # 'openclaw' = Use OpenClaw TTS first (high quality)
    # 'espeak' = Use espeak directly (fast, basic quality)
    TTS_ENGINE = 'openclaw'

    # ═══════════════════════════════════════════════════════════
    # LOGGING SETTINGS
    # ═══════════════════════════════════════════════════════════

    # Log file path
    # Can be relative (to script directory) or absolute
    # Examples:
    #   'voice_wake.log'  # Relative to script directory
    #   '/var/log/voice_wake.log'  # Absolute path (requires permissions)
    LOG_FILE = 'voice_wake.log'

    # Logging level
    # Options: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
    # DEBUG = Very detailed information (for troubleshooting)
    # INFO = General operational messages (recommended)
    # WARNING = Unexpected but recoverable issues
    # ERROR = Errors that don't stop the service
    LOG_LEVEL = 'INFO'

    # ═══════════════════════════════════════════════════════════
    # PERFORMANCE SETTINGS
    # ═══════════════════════════════════════════════════════════

    # Enable/disable audio feedback beep
    # True = Play beep when wake word detected
    # False = No audio feedback
    ENABLE_AUDIO_FEEDBACK = True

    # Feedback beep frequency (Hz)
    # 880 = A5 note (pleasant tone)
    # 440 = A4 note (middle A)
    # 1000-2000 = Higher pitch (more noticeable)
    FEEDBACK_FREQUENCY = 880

    # Feedback beep duration (seconds)
    # 0.1 = Short beep
    # 0.2 = Medium beep (default)
    # 0.3 = Long beep
    FEEDBACK_DURATION = 0.2

    # ═══════════════════════════════════════════════════════════
    # ADVANCED SETTINGS
    # ═══════════════════════════════════════════════════════════

    # Maximum number of retry attempts for API calls
    MAX_RETRIES = 3

    # Retry delay (seconds)
    RETRY_DELAY = 2

    # OpenClaw command timeout (seconds)
    OPENCLAW_TIMEOUT = 120

    # Speech recognition timeout (seconds)
    SPEECH_RECOGNITION_TIMEOUT = 30

    # TTS generation timeout (seconds)
    TTS_TIMEOUT = 30

    # Audio playback timeout (seconds)
    AUDIO_PLAYBACK_TIMEOUT = 10

    # MP3 playback timeout (seconds)
    MP3_PLAYBACK_TIMEOUT = 120

    # ═══════════════════════════════════════════════════════════
    # CUSTOM PROMPTS (OPTIONAL)
    # ═══════════════════════════════════════════════════════════

    # Prepend this text to all voice commands
    # Example: "Please answer in voice mode: {command}"
    COMMAND_PREFIX = ". Reply in voice mode."

    # Postpend this text to all voice commands
    COMMAND_SUFFIX = ""

    # ═══════════════════════════════════════════════════════════
    # DEVELOPMENT / DEBUGGING
    # ═══════════════════════════════════════════════════════════

    # Debug mode (enables additional logging)
    DEBUG = False

    # Save recorded audio for debugging
    # WARNING: This may use significant disk space
    SAVE_RECORDINGS = False

    # Recordings directory (used if SAVE_RECORDINGS = True)
    RECORDINGS_DIR = 'recordings'

    # ═══════════════════════════════════════════════════════════
    # END OF CONFIGURATION
    # ═══════════════════════════════════════════════════════════
