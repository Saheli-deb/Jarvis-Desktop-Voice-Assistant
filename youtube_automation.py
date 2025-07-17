import pyautogui
import pyttsx3

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate",200)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def control_youtube(action):
    key_map = {
        "play": "k",
        "pause": "k",
        "mute": "m",
        "full screen": "f",
        "theater mode": "t",
        "next video": "shift+n",
        "previous video": "shift+p",
        "increase speed": "shift+.",
        "decrease speed": "shift+,",
        "seek forward": "l",
        "seek backward": "j",
        "beginning": "0",
        "end": "9",
    }

    if action in key_map:
        if "+" in key_map[action]:
            mods = key_map[action].split("+")
            pyautogui.hotkey(*mods)
        else:
            pyautogui.press(key_map[action])
        speak(f"Performed {action} on YouTube")
    else:
        speak("Action not supported yet.")
