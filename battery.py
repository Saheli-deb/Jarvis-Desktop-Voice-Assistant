import psutil
import pyttsx3

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate",200)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def check_battery():
    battery = psutil.sensors_battery()
    if battery is None:
        speak("Sorry, I couldn't retrieve the battery status.")
        return
    percent = battery.percent
    plugged = battery.power_plugged
    status = "charging" if plugged else "not charging"
    speak(f"Battery is at {percent} percent and it is currently {status}.")
