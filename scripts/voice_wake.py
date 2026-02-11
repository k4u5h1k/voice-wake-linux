#!/usr/bin/env python3
"""
Voice Wake functionality for Linux with TTS responses
Uses OpenWakeWord for wake detection, SpeechRecognition for STT, and TTS for responses
Compatible with Raspberry Pi and other Linux systems
"""

import os
import sys
import signal
import json
import time
import logging
import subprocess
import threading
import numpy as np
import tempfile
import wave
from pathlib import Path
from typing import Optional

import openwakeword
from openwakeword.model import Model
import pyaudio
import speech_recognition as sr

# Configuration
class Config:
    # OpenWakeWord settings
    WAKE_WORD = 'hey_jarvis'  # Wake word to detect (available: alexa, hey_mycroft, hey_jarvis)
    DETECTION_THRESHOLD = 0.3  # Sensitivity (0.0-1.0)

    # OpenClaw settings - UPDATE THESE FOR YOUR SYSTEM
    OPENCLAW_CLI = 'openclaw'  # Path to openclaw CLI or use 'openclaw' if in PATH
    SESSION_ID = 'voice:wake:main'  # Consistent session key for multi-turn conversations

    # Audio settings
    AUDIO_DEVICE_INDEX = None  # None for default device
    SAMPLE_RATE = 16000
    CHUNK_SIZE = 1280  # 80ms chunks
    CHANNELS = 1

    # Recording settings
    RECORDING_TIMEOUT = 10  # seconds
    PHRASE_TIMEOUT = 3      # seconds

    # TTS settings
    ENABLE_TTS = True  # Set to False to disable spoken responses
    AUDIO_PLAYER = 'aplay'  # Command to play audio (aplay, paplay, etc.)
    MP3_PLAYER = 'ffplay'  # Command to play MP3 files (ffplay, mpg123, etc.)

    # Logging
    LOG_FILE = 'voice_wake.log'  # Log file path (relative to script or absolute)
    LOG_LEVEL = logging.INFO

# Setup logging
def setup_logging():
    """Setup logging configuration"""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Create log directory if it doesn't exist
    log_path = Path(Config.LOG_FILE)
    if not log_path.is_absolute():
        log_path = Path(__file__).parent / Config.LOG_FILE
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=Config.LOG_LEVEL,
        format=log_format,
        handlers=[
            logging.FileHandler(str(log_path)),
            logging.StreamHandler(sys.stdout)
        ]
    )

logger = logging.getLogger(__name__)

class VoiceWakeService:
    """Voice wake service class with TTS responses"""

    def __init__(self):
        self.wake_word_model = None
        self.recognizer = None
        self.microphone = None
        self.running = False
        self.recording = False
        self.audio_stream = None
        self.pyaudio_instance = None

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, sig, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {sig}, shutting down gracefully...")
        self.stop()
        sys.exit(0)

    def initialize_wake_word_detection(self):
        """Initialize OpenWakeWord model"""
        try:
            # Download and initialize the model
            logger.info("Initializing OpenWakeWord model...")

            # Initialize with default models
            self.wake_word_model = Model()

            logger.info("✅ OpenWakeWord model initialized successfully")
            # Check what attributes are available
            try:
                if hasattr(self.wake_word_model, 'model_names'):
                    logger.info(f"Available models: {self.wake_word_model.model_names}")
                else:
                    logger.info("Model initialized with default wake words")
            except Exception as e:
                logger.warning(f"Could not retrieve model names: {e}")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize OpenWakeWord: {e}")
            return False

    def initialize_speech_recognition(self):
        """Initialize speech recognition components"""
        try:
            # Initialize recognizer
            self.recognizer = sr.Recognizer()

            # Initialize microphone
            self.microphone = sr.Microphone(
                device_index=Config.AUDIO_DEVICE_INDEX,
                sample_rate=Config.SAMPLE_RATE
            )

            # Adjust for ambient noise
            logger.info("Adjusting for ambient noise...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)

            logger.info("✅ Speech recognition initialized")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize speech recognition: {e}")
            return False

    def initialize_audio_stream(self):
        """Initialize PyAudio stream for wake word detection"""
        try:
            self.pyaudio_instance = pyaudio.PyAudio()

            # List audio devices for debugging
            logger.info("Available audio devices:")
            for i in range(self.pyaudio_instance.get_device_count()):
                info = self.pyaudio_instance.get_device_info_by_index(i)
                logger.info(f"  {i}: {info['name']} (channels: {info['maxInputChannels']})")

            self.audio_stream = self.pyaudio_instance.open(
                format=pyaudio.paInt16,
                channels=Config.CHANNELS,
                rate=Config.SAMPLE_RATE,
                input=True,
                frames_per_buffer=Config.CHUNK_SIZE,
                input_device_index=Config.AUDIO_DEVICE_INDEX
            )

            logger.info(f"✅ Audio stream opened (device: {Config.AUDIO_DEVICE_INDEX or 'default'})")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize audio stream: {e}")
            return False

    def send_to_openclaw(self, text: str) -> Optional[str]:
        """Send transcribed text to OpenClaw and return response"""
        try:
            logger.info(f"Sending to OpenClaw: {text}")

            # Use openclaw CLI with JSON output
            cmd = [
                Config.OPENCLAW_CLI,
                'agent',
                '--session-id', Config.SESSION_ID,
                '--message', text,
                '--json'
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode != 0:
                logger.error(f"OpenClaw CLI failed: {result.stderr}")
                return None

            # Parse JSON response
            try:
                response = json.loads(result.stdout)

                # Extract the response text from the result
                if 'result' in response and 'payloads' in response['result']:
                    payloads = response['result']['payloads']
                    if payloads and len(payloads) > 0:
                        # Get the text from the first payload
                        response_text = payloads[0].get('text', '')
                        if response_text:
                            logger.info(f"✅ OpenClaw response: {response_text}")
                            return response_text

                logger.warning("No response text found in OpenClaw output")
                return None

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse OpenClaw JSON response: {e}")
                return None

        except subprocess.TimeoutExpired:
            logger.error("OpenClaw command timed out")
            return None
        except Exception as e:
            logger.error(f"Failed to send to OpenClaw: {e}")
            return None

    def play_wake_feedback(self):
        """Play audio feedback when wake word is detected"""
        try:
            # Generate a simple beep sound
            sample_rate = 16000
            duration = 0.2  # 100ms beep
            frequency = 880  # A5 note (pleasant tone)

            # Generate the audio samples
            t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
            audio_data = (0.5 * np.sin(2 * np.pi * frequency * t) * 32767).astype(np.int16)

            # Create a temporary WAV file
            with tempfile.NamedTemporaryFile(mode='wb', suffix='.wav', delete=False) as temp_file:
                temp_filename = temp_file.name

                # Write WAV file header
                with wave.open(temp_file, 'wb') as wav_file:
                    wav_file.setnchannels(1)  # Mono
                    wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
                    wav_file.setframerate(sample_rate)
                    wav_file.writeframes(audio_data.tobytes())

            # Play the sound using aplay
            try:
                subprocess.run(['aplay', '-q', temp_filename], check=True, timeout=2)
                logger.debug("✅ Audio feedback played successfully")
            except subprocess.TimeoutExpired:
                logger.warning("Audio feedback playback timed out")
            except subprocess.CalledProcessError as e:
                logger.warning(f"Failed to play audio feedback: {e}")
            except FileNotFoundError:
                logger.warning("aplay not found - audio feedback disabled")
            finally:
                # Clean up the temporary file
                try:
                    os.unlink(temp_filename)
                except:
                    pass

        except Exception as e:
            logger.warning(f"Failed to generate/play audio feedback: {e}")

    def text_to_speech(self, text: str) -> Optional[str]:
        """Convert text to speech and return audio file path"""
        try:
            # Try OpenClaw CLI TTS first
            cmd = [
                Config.OPENCLAW_CLI,
                'tts',
                '--text', text
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0 and 'MEDIA:' in result.stdout:
                # Extract the media path
                media_path = result.stdout.split('MEDIA:')[1].strip()
                logger.info(f"✅ TTS generated: {media_path}")
                return media_path
            else:
                logger.warning("OpenClaw TTS not available, using espeak fallback")

        except FileNotFoundError:
            logger.warning("OpenClaw CLI not found, using espeak fallback")
        except Exception as e:
            logger.warning(f"OpenClaw TTS failed ({e}), using espeak fallback")

        # Fallback to espeak
        try:
            temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            temp_file.close()

            subprocess.run([
                'espeak',
                '-v', 'en-us',
                '-w', temp_file.name,
                text
            ], check=True, timeout=30)

            logger.info(f"✅ TTS generated (espeak): {temp_file.name}")
            return temp_file.name

        except FileNotFoundError:
            logger.error("espeak not found - cannot speak responses")
            return None
        except Exception as e:
            logger.error(f"Espeak TTS failed: {e}")
            return None

    def play_audio(self, audio_path: str) -> bool:
        """Play audio file using configured player"""
        try:
            logger.info(f"🔊 Playing audio: {audio_path}")

            result = subprocess.run(
                [Config.AUDIO_PLAYER, audio_path],
                capture_output=True,
                timeout=10
            )

            if result.returncode == 0:
                logger.info("✅ Audio playback completed")
                return True
            else:
                logger.error(f"Audio playback failed: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            logger.error("Audio playback timed out")
            return False
        except FileNotFoundError:
            logger.error(f"Audio player '{Config.AUDIO_PLAYER}' not found")
            return False
        except Exception as e:
            logger.error(f"Failed to play audio: {e}")
            return False

    def play_mp3(self, mp3_path: str) -> bool:
        """Play MP3 file using configured MP3 player"""
        try:
            logger.info(f"🎵 Playing MP3: {mp3_path}")

            # Use ffplay with auto-close after playback
            result = subprocess.run(
                [Config.MP3_PLAYER, '-nodisp', '-autoexit', mp3_path],
                capture_output=True,
                timeout=120  # Longer timeout for MP3 files
            )

            if result.returncode == 0:
                logger.info("✅ MP3 playback completed")
                return True
            else:
                logger.error(f"MP3 playback failed: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            logger.error("MP3 playback timed out")
            return False
        except FileNotFoundError:
            logger.error(f"MP3 player '{Config.MP3_PLAYER}' not found")
            return False
        except Exception as e:
            logger.error(f"Failed to play MP3: {e}")
            return False

    def speak_response(self, text: str):
        """Convert text to speech and play it, or play MP3 if response is MEDIA: path"""
        if not Config.ENABLE_TTS:
            logger.info(f"Response (not spoken): {text}")
            return

        try:
            # Check if response is a MEDIA: path (MP3 file)
            if text.startswith('MEDIA:'):
                # Extract MP3 file path
                mp3_path = text[6:].strip()  # Remove "MEDIA:" prefix
                logger.info(f"🎵 Detected MP3 response: {mp3_path}")

                # Play MP3 directly
                if os.path.exists(mp3_path):
                    success = self.play_mp3(mp3_path)
                    if success:
                        logger.info("✅ MP3 playback completed")
                        return
                    else:
                        logger.warning("MP3 playback failed, falling back to TTS")
                        # If MP3 playback fails, extract text from MEDIA line
                        # The format is typically "MEDIA:<path>" followed by the text
                        # But if it's just the MEDIA line, we have no text to speak
                        logger.info("No text content to speak from MEDIA response")
                        return
                else:
                    logger.warning(f"MP3 file not found: {mp3_path}")
                    return

            # Regular text response - use TTS
            # Generate speech
            audio_path = self.text_to_speech(text)

            if audio_path and os.path.exists(audio_path):
                # Play the audio
                self.play_audio(audio_path)

                # Clean up temporary file (except for TTS tool outputs which manage their own lifecycle)
                try:
                    if not audio_path.startswith('/tmp/tts-'):  # Don't delete TTS tool temp files
                        os.unlink(audio_path)
                except:
                    pass
            else:
                logger.warning("Could not generate or find audio file")

        except Exception as e:
            logger.error(f"Failed to speak response: {e}")

    def record_and_transcribe(self):
        """Record audio after wake word, transcribe, and handle response"""
        if self.recording:
            return

        self.recording = True
        logger.info("🎙️  Wake word detected! Recording for 10 seconds...")

        try:
            # Record for exactly 10 seconds
            with self.microphone as source:
                logger.info("Recording... You have 10 seconds to speak your command")
                audio = self.recognizer.record(source, duration=10)
                logger.info("Recording finished!")

            self.play_wake_feedback()

            # Try to transcribe
            logger.info("Transcribing...")
            try:
                # Use Google Web Speech API (free tier)
                text = self.recognizer.recognize_google(audio)

                if text and text.strip():
                    logger.info(f"Transcribed: '{text}'")

                    # Send to OpenClaw and get response
                    response_text = self.send_to_openclaw(text.strip() + ". Reply in voice mode.")

                    if response_text:
                        logger.info("✅ Command processed successfully")

                        # Speak the response
                        self.speak_response(response_text)
                    else:
                        logger.warning("⚠️  No response from OpenClaw")
                else:
                    logger.info("No speech detected or transcription empty")

            except sr.UnknownValueError:
                logger.info("Could not understand audio")
            except sr.RequestError as e:
                logger.error(f"Speech recognition error: {e}")

        except Exception as e:
            logger.error(f"Error during recording/transcription: {e}")

        finally:
            self.recording = False
            logger.info("Ready for next wake word...")

    def start(self):
        """Start the voice wake service"""
        logger.info("🚀 Starting Voice Wake Service with TTS...")

        # Initialize components
        if not self.initialize_wake_word_detection():
            logger.error("Failed to initialize wake word detection")
            return False

        if not self.initialize_speech_recognition():
            logger.error("Failed to initialize speech recognition")
            return False

        if not self.initialize_audio_stream():
            logger.error("Failed to initialize audio stream")
            return False

        logger.info("✅ All components initialized successfully")
        logger.info(f"🎯 Say '{Config.WAKE_WORD}' to wake up, then speak your command")
        logger.info(f"🔊 TTS is {'enabled' if Config.ENABLE_TTS else 'disabled'}")

        self.running = True

        last_run = 0

        # Main wake word detection loop
        try:
            while self.running:
                try:
                    # Read audio data
                    audio_data = self.audio_stream.read(
                        Config.CHUNK_SIZE,
                        exception_on_overflow=False
                    )

                    # Convert to numpy array
                    audio_array = np.frombuffer(audio_data, dtype=np.int16)

                    # Get wake word predictions
                    predictions = self.wake_word_model.predict(audio_array)

                    # Check if configured wake word detected
                    if Config.WAKE_WORD in predictions:
                        confidence = predictions[Config.WAKE_WORD]
                        if confidence > Config.DETECTION_THRESHOLD:
                            logger.info(f"🎯 Wake word '{Config.WAKE_WORD}' detected (confidence: {confidence:.2f})")

                            if time.time() - last_run > 3:
                                # Play audio feedback
                                self.play_wake_feedback()

                                # Start recording in a separate thread
                                threading.Thread(
                                    target=self.record_and_transcribe,
                                    daemon=True
                                ).start()

                                last_run = time.time()

                except Exception as e:
                    if self.running:  # Only log errors if we're still supposed to be running
                        logger.error(f"Error in main loop: {e}")
                        time.sleep(0.1)  # Brief pause before continuing

        except Exception as e:
            logger.error(f"Fatal error in main loop: {e}")
            return False

        logger.info("Voice Wake Service stopped")
        return True

    def stop(self):
        """Stop the voice wake service"""
        logger.info("Stopping Voice Wake Service...")
        self.running = False

        # Cleanup resources
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
            self.audio_stream = None

        if self.pyaudio_instance:
            self.pyaudio_instance.terminate()
            self.pyaudio_instance = None

        if self.wake_word_model:
            self.wake_word_model = None

        logger.info("✅ Voice Wake Service stopped successfully")

def main():
    """Main entry point"""
    setup_logging()
    logger.info("=" * 70)
    logger.info("🎙️  Voice Wake Service with TTS for Linux")
    logger.info("=" * 70)

    # Create and start service
    service = VoiceWakeService()

    try:
        success = service.start()
        if not success:
            logger.error("Service failed to start properly")
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        service.stop()

if __name__ == "__main__":
    main()
