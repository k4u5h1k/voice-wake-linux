# System Architecture

Voice Wake Linux is designed with a modular, extensible architecture that separates concerns and allows for easy customization.

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        Voice Wake Linux                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Wake Word  │───▶│   Speech     │───▶│    OpenClaw  │  │
│  │  Detection   │    │ Recognition  │    │   AI Engine  │  │
│  │              │    │              │    │              │  │
│  │  OpenWakeWord│    │ Google STT   │    │   Webhook    │  │
│  └──────────────┘    └──────────────┘    └──────┬───────┘  │
│         │                                       │           │
│         │                                       │           │
│         ▼                                       ▼           │
│  ┌──────────────┐                        ┌──────────────┐  │
│  │   Audio      │                        │   Response   │  │
│  │   Feedback   │                        │  Processing  │  │
│  │              │                        │              │  │
│  │  Beep Sound  │                        │  Session Mgmt│  │
│  └──────────────┘                        └──────┬───────┘  │
│                                                 │           │
│                                                 ▼           │
│                                          ┌──────────────┐  │
│                                          │   Text-to    │  │
│                                          │   Speech     │  │
│                                          │              │  │
│                                          │  espeak/TTS  │  │
│                                          └──────┬───────┘  │
│                                                 │           │
│                                                 ▼           │
│                                          ┌──────────────┐  │
│                                          │   Audio      │  │
│                                          │   Output     │  │
│                                          │              │  │
│                                          │  aplay/paplay│  │
│                                          └──────────────┘  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Wake Word Detection

**Technology**: OpenWakeWord

**Purpose**: Detects the wake word ("Hey Jarvis") in continuous audio stream

**Key Features**:
- Low-latency detection (< 200ms)
- Pre-trained models for common wake words
- Configurable sensitivity threshold
- Runs entirely on-device (no network required)

**Process**:
1. Reads audio in 80ms chunks (1280 samples @ 16kHz)
2. Uses neural network to predict wake words
3. Checks confidence score against threshold
4. Triggers recording when threshold exceeded

### 2. Audio Processing

**Technology**: PyAudio + ALSA

**Purpose**: Captures and plays audio

**Key Features**:
- Continuous audio streaming for wake word detection
- 10-second fixed recording for commands
- Audio feedback beeps
- Support for multiple audio devices

**Audio Flow**:
```
Microphone → PyAudio Stream → Wake Word Detection
                                   ↓
                              Wake Word Detected
                                   ↓
                          Fixed 10-Second Recording
                                   ↓
                            Speech Recognition
```

### 3. Speech Recognition

**Technology**: Google Web Speech API (via SpeechRecognition library)

**Purpose**: Transcribes recorded audio to text

**Key Features**:
- High accuracy (> 95% for clear speech)
- Supports multiple languages
- Free tier available
- Fallback handling for errors

**Process**:
1. Records 10 seconds of audio
2. Sends to Google Speech API
3. Receives transcription text
4. Handles errors gracefully

### 4. AI Integration

**Technology**: OpenClaw

**Purpose**: Processes voice commands and generates responses

**Key Features**:
- Session continuity (multi-turn conversations)
- JSON-based API
- Support for text and MP3 responses
- Configurable session keys

**Webhook Flow**:
```python
POST /hooks/agent
{
    "message": "What time is it?",
    "sessionKey": "voice:wake:main",
    "wakeMode": "now"
}

Response:
{
    "result": {
        "payloads": [
            { "text": "The current time is 5:58 PM" }
        ]
    }
}
```

### 5. Text-to-Speech

**Technology**: espeak / OpenClaw TTS

**Purpose**: Converts AI responses to spoken audio

**Key Features**:
- Primary: OpenClaw TTS (high quality)
- Fallback: espeak (always available)
- MP3 response support
- Configurable audio players

**Process**:
1. Check if response is MEDIA: path (MP3)
2. If MP3: Play directly with ffplay
3. If text: Generate speech with OpenClaw TTS or espeak
4. Play audio file with aplay/paplay

### 6. Session Management

**Technology**: Custom session key system

**Purpose**: Maintains conversation context across multiple commands

**Key Features**:
- Consistent session key: `voice:wake:main`
- Multi-turn conversation support
- Context-aware responses
- Session isolation

**Benefits**:
- User can ask follow-up questions
- AI remembers previous context
- Natural conversation flow

### 7. Systemd Service

**Technology**: systemd user service

**Purpose**: Runs voice wake as a background service

**Key Features**:
- Auto-start on login
- Auto-restart on failure
- Log management (journal + file)
- Easy service management

**Service Lifecycle**:
```
Start → Initialize → Detect Wake Words → Process Commands → Loop
  ↓         ↓              ↓                  ↓           ↓
Stop   Cleanup      Stop Detection    Complete      Auto-restart
```

## Data Flow

### Complete Command Flow

```
1. User says "Hey Jarvis"
   ↓
2. Wake word detected (confidence > threshold)
   ↓
3. Audio feedback beep played
   ↓
4. System records for 10 seconds
   ↓
5. Audio sent to Google Speech API
   ↓
6. Transcription received: "what time is it"
   ↓
7. Request sent to OpenClaw with session key
   ↓
8. OpenClaw processes with session context
   ↓
9. Response received: "The current time is 5:58 PM"
   ↓
10. TTS generates audio file
   ↓
11. Audio played to user
   ↓
12. System returns to wake word detection
```

### Session Continuity Flow

```
Command 1: "What's the capital of France?"
  ↓
Session: voice:wake:main
  ↓
Response: "The capital of France is Paris"

Command 2: "And what's the population?"
  ↓
Session: voice:wake:main (same session)
  ↓
Context: Previous question about Paris
  ↓
Response: "Paris has a population of about 2.1 million people"
```

## Configuration Architecture

### Configuration Layers

1. **Default Configuration** (in `voice_wake.py`)
   - Built-in defaults for all settings
   - Hardcoded in the script

2. **User Configuration** (in `config.py`)
   - User-customizable settings
   - Overrides defaults
   - Optional file

3. **Runtime Configuration**
   - Environment variables (future)
   - Command-line arguments (future)
   - Dynamic settings (future)

### Priority Order

```
Runtime Settings > User Config > Defaults
```

## Error Handling

### Error Recovery Strategy

```
Component Failure → Log Error → Fallback → Continue
                        ↓
                  Recovery Attempt
                        ↓
                    Success/Retry Limit
```

### Fallback Mechanisms

1. **TTS Fallback**: OpenClaw TTS → espeak
2. **Audio Player Fallback**: aplay → paplay → (error)
3. **Speech Recognition**: Google API → (retry) → (error message)
4. **AI Response**: OpenClaw → (retry) → (error message)

## Performance Optimization

### Wake Word Detection
- **Chunk Size**: 1280 samples (80ms @ 16kHz)
- **Sample Rate**: 16kHz (optimal for speech)
- **Threshold**: 0.3 (balance between sensitivity and false positives)
- **Cooldown**: 3 seconds between detections

### Audio Processing
- **Buffer Size**: Optimized for low latency
- **Threading**: Recording runs in separate thread
- **Async Operations**: Non-blocking where possible

### Resource Usage
- **CPU**: ~5-10% on modern hardware
- **Memory**: ~50-100MB (Python + models)
- **Network**: Only for speech recognition and AI

## Security Considerations

### Data Privacy
- Audio recordings are not stored (processed in memory)
- Transcripts are logged (can be disabled)
- AI responses are cached only for session duration

### Network Security
- Uses HTTPS for all API calls
- No authentication required (Google Speech free tier)
- OpenClaw uses local webhook (localhost)

### Access Control
- Runs as non-privileged user
- Systemd user service (no root access)
- No system file modifications

## Extensibility

### Adding New Wake Words
1. Train custom model with OpenWakeWord
2. Add to model initialization
3. Update configuration

### Adding New AI Services
1. Modify `send_to_openclaw()` method
2. Implement API client
3. Adapt response parsing

### Adding New TTS Engines
1. Modify `text_to_speech()` method
2. Implement engine-specific logic
3. Add fallback handling

### Adding Custom Features
- Plugin architecture (future)
- Web interface (future)
- Mobile app integration (future)

## Monitoring and Debugging

### Logging Levels
- **DEBUG**: Detailed information for diagnostics
- **INFO**: General operational messages
- **WARNING**: Unexpected but recoverable issues
- **ERROR**: Errors that don't stop the service
- **CRITICAL**: Serious errors that may stop the service

### Log Locations
- **System Journal**: `journalctl --user -u voice-wake.service`
- **Application Log**: `voice_wake.log`
- **System Log**: `/var/log/syslog` (via logger)

### Health Checks
- Service status: `systemctl --user status voice-wake.service`
- Audio devices: `arecord -l` and `aplay -l`
- Network connectivity: Test API endpoints
- Resource usage: `top` or `htop`

## Future Architecture Improvements

1. **Modular Plugin System**
   - Pluggable wake word detectors
   - Swappable AI backends
   - Multiple TTS engines

2. **Web Interface**
   - Configuration UI
   - Real-time monitoring
   - Log viewing

3. **API Server**
   - REST API for control
   - WebSocket for events
   - Remote monitoring

4. **Multi-User Support**
   - User profiles
   - Personalized settings
   - Separate sessions

5. **Machine Learning**
   - Adaptive threshold
   - Voice recognition
   - Personalized responses
