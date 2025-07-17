import pyttsx3
import os

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate",200)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def handle_system_command(command):
    if "shutdown" in command:
        speak("Shutting down the system.")
        os.system("shutdown /s /t 1")
    elif "restart" in command:
        speak("Restarting the system.")
        os.system("shutdown /r /t 1")
    elif "log off" in command:
        speak("Logging off.")
        os.system("shutdown -l")
    else:
        speak("Unknown system command.")
