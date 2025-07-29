#!/usr/bin/env python3
"""
Microphone Test Script
Tests if your microphone is working properly with speech recognition.
"""

import speech_recognition as sr
import time

def test_microphone():
    """Test microphone and speech recognition"""
    r = sr.Recognizer()
    
    print("🎤 MICROPHONE TEST")
    print("=" * 50)
    
    # List available microphones
    print("Available microphones:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"  {index}: {name}")
    
    print("\n" + "=" * 50)
    
    # Test microphone
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... Please wait...")
            r.adjust_for_ambient_noise(source, duration=2)
            
            print("🎤 Please speak something now...")
            print("Listening for 5 seconds...")
            
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            
            print("Processing speech...")
            query = r.recognize_google(audio, language='en-in')
            
            print(f"✅ SUCCESS! You said: '{query}'")
            return True
            
    except sr.WaitTimeoutError:
        print("❌ No speech detected within timeout")
        return False
    except sr.UnknownValueError:
        print("❌ Could not understand what you said")
        return False
    except sr.RequestError as e:
        print(f"❌ Could not request results; {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing microphone and speech recognition...")
    success = test_microphone()
    
    if success:
        print("\n✅ Microphone test PASSED!")
        print("Your microphone is working correctly.")
    else:
        print("\n❌ Microphone test FAILED!")
        print("Please check your microphone settings.")
    
    input("\nPress Enter to exit...") 