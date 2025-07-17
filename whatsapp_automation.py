import pyautogui
import pyttsx3
import speech_recognition
import time
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate",200)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def takeCommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 0.5

        r.energy_threshold = 100
        audio = r.listen(source, 0, 4)

    try:
        print("Understanding..")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
        return query.lower()  # Ensure lowercase for consistency
    except Exception as e:
        print("Say that again")
        return "None"

def send_whatsapp_message_auto():
    speak("Who do you want to send a message to?")
    contact = takeCommand().lower()

    speak("What should I send?")
    message = takeCommand()

    # Open WhatsApp (Shortcut for Windows: Win + S, then search "WhatsApp")
    pyautogui.hotkey('win', 's')
    time.sleep(1)
    pyautogui.write('WhatsApp')  # Type "WhatsApp"
    time.sleep(1)
    pyautogui.press('enter')  # Press Enter to open
    time.sleep(5)  # Wait for WhatsApp to open

    # Search for the contact
    pyautogui.hotkey('ctrl', 'f')  # Open search bar
    time.sleep(1)
    pyautogui.write(contact)  # Type contact name
    time.sleep(2)
    pyautogui.press('enter')  # Open chat

    # Type and send the message
    time.sleep(2)
    pyautogui.write(message)  # Type message
    time.sleep(1)
    pyautogui.press('enter')  # Send message

    speak(f"Message sent to {contact}.")