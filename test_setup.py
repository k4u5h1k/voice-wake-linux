#!/usr/bin/env python3
"""
Voice Wake Linux - Setup Test Script
Tests if all dependencies are properly installed and configured
"""

import sys
import subprocess
import importlib.util
from pathlib import Path

def test_python_version():
    """Test if Python version is compatible"""
    print("Testing Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible (requires Python 3.8+)")
        return False

def test_python_module(module_name):
    """Test if a Python module can be imported"""
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is not None:
            print(f"✅ {module_name} is available")
            return True
        else:
            print(f"❌ {module_name} is not installed")
            return False
    except Exception as e:
        print(f"❌ Error checking {module_name}: {e}")
        return False

def test_system_command(command):
    """Test if a system command is available"""
    try:
        result = subprocess.run(['which', command], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {command} is available at {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {command} is not found in PATH")
            return False
    except Exception as e:
        print(f"❌ Error checking {command}: {e}")
        return False

def test_audio_devices():
    """Test if audio devices are available"""
    print("\nTesting audio devices...")
    
    # Test microphones
    try:
        result = subprocess.run(['arecord', '-l'], capture_output=True, text=True)
        if result.returncode == 0:
            if 'card' in result.stdout.lower():
                print("✅ Microphone devices found:")
                for line in result.stdout.split('\n'):
                    if 'card' in line.lower():
                        print(f"   {line.strip()}")
            else:
                print("⚠️  No microphone devices found")
                return False
        else:
            print("❌ Could not list microphone devices")
            return False
    except Exception as e:
        print(f"❌ Error testing microphones: {e}")
        return False
    
    # Test speakers
    try:
        result = subprocess.run(['aplay', '-l'], capture_output=True, text=True)
        if result.returncode == 0:
            if 'card' in result.stdout.lower():
                print("✅ Speaker devices found:")
                for line in result.stdout.split('\n'):
                    if 'card' in line.lower():
                        print(f"   {line.strip()}")
            else:
                print("⚠️  No speaker devices found")
                return False
        else:
            print("❌ Could not list speaker devices")
            return False
    except Exception as e:
        print(f"❌ Error testing speakers: {e}")
        return False
    
    return True

def test_internet_connection():
    """Test internet connection (required for speech recognition)"""
    print("\nTesting internet connection...")
    try:
        import urllib.request
        urllib.request.urlopen('https://www.google.com', timeout=5)
        print("✅ Internet connection is available")
        return True
    except Exception as e:
        print(f"❌ Internet connection test failed: {e}")
        print("   Note: Internet is required for speech recognition")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Voice Wake Linux - Setup Test")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 0
    
    # Test Python version
    total_tests += 1
    if test_python_version():
        tests_passed += 1
    
    print("\nTesting Python modules...")
    required_modules = [
        'numpy',
        'pyaudio',
        'speech_recognition',
        'openwakeword'
    ]
    
    for module in required_modules:
        total_tests += 1
        if test_python_module(module):
            tests_passed += 1
    
    print("\nTesting system commands...")
    required_commands = [
        'aplay',
        'arecord',
        'espeak'
    ]
    
    optional_commands = [
        'ffplay',
        'paplay'
    ]
    
    for command in required_commands:
        total_tests += 1
        if test_system_command(command):
            tests_passed += 1
    
    print("\nTesting optional commands...")
    for command in optional_commands:
        if test_system_command(command):
            print(f"✅ {command} is available (good for enhanced functionality)")
        else:
            print(f"ℹ️  {command} not found (optional, can enhance functionality)")
    
    # Test audio devices
    total_tests += 1
    if test_audio_devices():
        tests_passed += 1
    
    # Test internet connection
    total_tests += 1
    if test_internet_connection():
        tests_passed += 1
    
    print("\n" + "=" * 60)
    print("Test Results")
    print("=" * 60)
    print(f"Passed: {tests_passed}/{total_tests} tests")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Your system is ready for Voice Wake Linux.")
        print("\nNext steps:")
        print("1. Edit config.py to customize settings")
        print("2. Run: ./scripts/voice_wake.py")
        print("3. Say 'Hey Jarvis' to test wake word detection")
        return True
    else:
        print("⚠️  Some tests failed. Please install missing dependencies.")
        print("\nTo install missing dependencies:")
        print("- Run the install script: ./install.sh")
        print("- Or install manually using your package manager")
        print("- Check the README.md for detailed instructions")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)