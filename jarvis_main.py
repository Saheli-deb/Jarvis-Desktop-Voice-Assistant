# import pyttsx3
# import speech_recognition
# import requests
# from bs4 import BeautifulSoup
# import datetime
# import pyautogui
# import os
# import my_keyboard
# import random
# import webbrowser
# import NewsRead
# import pywhatkit as kit
# import time
# import subprocess
# import pyautogui
# import ollama
# import ast
# import traceback
# # from ultralytics import Yolo
# # from pyler import notification
# from pygame import mixer
# from emotion_detection import get_combined_emotion, play_emotion_response

# import smtplib
# from INTRO import play_gif

# engine = pyttsx3.init("sapi5")
# voices = engine.getProperty("voices")
# engine.setProperty("voice", voices[0].id)
# engine.setProperty("rate", 300) 

# # def speak(audio):
# #     engine.say(audio)
# #     engine.runAndWait()
# def speak(audio, emotion=None):
#     """Enhanced speak function with emotion-based modulation"""
#     if emotion == "sad":
#         engine.setProperty("rate", base_rate - 30)  # Slower for sadness
#     elif emotion == "angry":
#         engine.setProperty("rate", base_rate + 40)  # Faster for urgency
#     elif emotion == "happy":
#         engine.setProperty("rate", base_rate + 20)  # More energetic
#     else:
#         engine.setProperty("rate", base_rate)
    
#     engine.say(audio)
#     engine.runAndWait()


# def check_password():
#     """Function to verify password before starting Jarvis"""
#     try:
#         with open("password.txt", "r") as pw_file:
#             pw = pw_file.read().strip()  # Remove spaces/newlines
#             print

#         for i in range(3):  # Allow 3 attempts
#             user_pw = input("Enter Password to open Jarvis: ").strip()

#             if user_pw == pw:
#                 print("WELCOME SIR! PLZ SPEAK [WAKE UP] TO LOAD ME UP")
#                 return True
#             elif i == 2:
#                 print("Too many incorrect attempts. Exiting...")
#                 exit()
#             else:
#                 print("Incorrect Password. Try Again.")

#     except FileNotFoundError:
#         print("Error: password.txt not found. Please create the file.")
#         exit()
# play_gif()


# def takeCommand():
#     r = speech_recognition.Recognizer()
#     with speech_recognition.Microphone() as source:
#         print("Listening.....")
#         r.pause_threshold = 0.5

#         r.energy_threshold = 100
#         audio = r.listen(source, 0, 4)

#     try:
#         print("Understanding..")
#         query = r.recognize_google(audio, language='en-in')
#         print(f"You Said: {query}\n")
#         return query.lower()  # Ensure lowercase for consistency
#     except Exception as e:
#         print("Say that again")
#         return "None"
# # def takeCommand():
# #     """Enhanced to include emotion detection"""
# #     emotion = None
# #     # Only detect emotion if not in LLaMA mode
# #     if not hasattr(takeCommand, 'in_llama_mode') or not takeCommand.in_llama_mode:
# #         emotion = get_combined_emotion()
# #         print(f"[SYSTEM] Detected Emotion: {emotion}")
# #         if emotion != "neutral":
# #             response = play_emotion_response(emotion)
# #             if response:
# #                 speak(response, emotion)

# #     r = sr.Recognizer()
# #     with sr.Microphone() as source:
# #         print("Listening.....")
# #         r.pause_threshold = 0.5
# #         r.energy_threshold = 100
# #         audio = r.listen(source, 0, 4)

# #     try:
# #         print("Understanding..")
# #         query = r.recognize_google(audio, language='en-in')
# #         print(f"You Said: {query}\n")
# #         return query.lower(), emotion  # Now returns both query and emotion
# #     except Exception as e:
# #         print("Say that again")
# #         return "None", "neutral"
# # alarm set 
# def alarm(query):
#      timehere = open("Alarmtext.txt","a")
#      timehere.write(query)
#      timehere.close()
#      os.startfile("alarm.py")
# # ai mode
# def chat_with_llama2():
#     speak("Hey I am your personal jarvis assistant. Say 'back to normal Jarvis' or 'exit' to go back.")
#     messages = [{"role": "system", "content": "You are Jarvis's AI assistant, helpful and concise."}]
    
#     while True:
#         user_input = takeCommand()
        
#         if user_input == "none":
#             continue

#         # exit 
#         if "back to normal jarvis" in user_input or "exit" in user_input:
#             speak("Exiting LLaMA 2 mode. Back to normal Jarvis.")
#             break

#         messages.append({"role": "user", "content": user_input})
        
#         try:
#             response = ollama.chat(model="llama2", messages=messages)
#             reply = response["message"]["content"]
#             messages.append({"role": "assistant", "content": reply})
#             print(f"LLaMA 2: {reply}")
#             speak(reply)
#         except Exception as e:
#             print("Error:", e)
#             speak("There was an error talking to LLaMA 2.")
# # weather report
# def get_weather(city="Delhi"):  
#     api_key = "cf9b51d9e6eaa91fd1a10945e1c928d9"  
#     base_url = "http://api.openweathermap.org/data/2.5/weather?"
#     complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"

#     response = requests.get(complete_url)
#     data = response.json()

#     if data["cod"] == 200:  
#         temp = data["main"]["temp"]
#         description = data["weather"][0]["description"]
#         speak(f"The current temperature in {city} is {temp} degrees Celsius with {description}.")
#     else:
#         speak("Sorry, I couldn't fetch the weather details.")
# # whatsapp automation
# def send_whatsapp_message_auto():
#     speak("Who do you want to send a message to?")
#     contact = takeCommand().lower()

#     speak("What should I send?")
#     message = takeCommand()

#     # Open WhatsApp (Shortcut for Windows: Win + S, then search "WhatsApp")
#     pyautogui.hotkey('win', 's')
#     time.sleep(1)
#     pyautogui.write('WhatsApp')  # Type "WhatsApp"
#     time.sleep(1)
#     pyautogui.press('enter')  # Press Enter to open
#     time.sleep(5)  # Wait for WhatsApp to open

#     # Search for the contact
#     pyautogui.hotkey('ctrl', 'f')  # Open search bar
#     time.sleep(1)
#     pyautogui.write(contact)  # Type contact name
#     time.sleep(2)
#     pyautogui.press('enter')  # Open chat

#     # Type and send the message
#     time.sleep(2)
#     pyautogui.write(message)  # Type message
#     time.sleep(1)
#     pyautogui.press('enter')  # Send message

#     speak(f"Message sent to {contact}.")

# if __name__ == "__main__": 
#      if check_password(): 
#       while True:  
#         query = takeCommand()
#         #  query, emotion = takeCommand()
#         # if face_login():  # Only activate Jarvis if face is recognized
#         #  speak("Jarvis is ready to assist you.")
#         if "wake up" in query:
#             from GreetMe import greetMe
#             greetMe()

#             while True:
#                 query = takeCommand()

#                 if "go to sleep" in query:  # ✅ Fixed condition
#                     speak("Ok sir, You can call me anytime")
#                     print("Sleeping mode activated.")  
#                     break  # Exits only after speaking    

#                 elif "click my photo" in query:
#                         pyautogui.press("win")
#                         time.sleep(1)
#                         pyautogui.write("camera", interval=0.1)
#                         time.sleep(1)
#                         pyautogui.press("enter")
#                         time.sleep(3)
#                         speak("SMILE")
#                         time.sleep(1)
#                         pyautogui.press("enter")
#                 elif "bot mode" in query or "jarvis assistant" in query:
#                     # chat_with_llama2()
#                     takeCommand.in_llama_mode = True  # Disable emotion detection
#                     chat_with_llama2()
#                     takeCommand.in_llama_mode = False


#                 elif "hello" in query:
#                         if emotion == "happy":
#                             speak("You sound cheerful today! How can I help?", emotion)
#                         elif emotion == "sad":
#                             speak("I sense you're feeling down. What's wrong?", emotion)
#                         else:
#                             speak("Hello sir, how may I assist you?", emotion)
                            
#                 elif "i am fine" in query:
#                         speak("That's great to hear!", emotion)
                        
#                 elif "how are you" in query:
#                         if emotion == "happy":
#                             speak("I'm wonderful seeing you happy!", emotion)
#                         else:
#                             speak("I'm functioning optimally, sir", emotion)
#                 # elif "hello" in query:
#                 #     speak("Hello sir, how are you?")
#                 # elif "i am fine" in query:
#                 #     speak("That's great, sir")
#                 # elif "how are you" in query:
#                 #     speak("Perfect, sir")
#                 elif "thank you" in query:
#                     speak("You're welcome, sir")
#                 elif "tired" in query:
#                    speak("Playing your favourite songs, sir")
#                    a = (1,2,3)
#                    b = random.choice(a)
#                    if b==1:
#                     webbrowser.open("https://www.youtube.com/watch?v=TVbI55pDdaI")
#                 elif "news" in query:
#                   from NewsRead import latestnews
#                   latestnews()
#                 elif "send whatsapp" in query or "message on whatsapp" in query:
#                  send_whatsapp_message_auto()
#                 elif "schedule my day" in query:
#                   tasks = [] #Empty list 
#                   speak("Do you want to clear old tasks (Plz speak YES or NO)")
#                   query = takeCommand().lower()
#                   if "yes" in query:
#                    file = open("tasks.txt","w")
#                    file.write(f"") 
#                    file.close()
#                    no_tasks = int(input("Enter the no. of tasks :- "))
#                    i = 0
#                    for i in range(no_tasks):
#                       tasks.append(input("Enter the task :- "))
#                       file = open("tasks.txt","a")
#                       file.write(f"{i}. {tasks[i]}\n")
#                       file.close()
#                 elif "no" in query:
#                      i = 0
#                      no_tasks = int(input("Enter the no. of tasks :- "))
#                      for i in range(no_tasks):
#                         tasks.append(input("Enter the task :- "))
#                         file = open("tasks.txt","a")
#                         file.write(f"{i}. {tasks[i]}\n")
#                         file.close()
#                 # elif "show my schedule" in query:
#                 #   file = open("tasks.txt","r")
#                 #   content = file.read()
#                 #   file.close()
#                 #   mixer.init()
#                 #   mixer.music.load("notification.mp3")
#                 #   mixer.music.play()
#                 #   notification.notify(
#                 #   title = "My schedule :-",
#                 #   message = content,
#                 #   timeout = 15
#                 # )
                
#                 elif "pause" in query:
#                  pyautogui.press("k")
#                  speak("video paused")
#                 elif "play" in query:
#                  pyautogui.press("k")
#                  speak("video played")
#                 elif "mute" in query:
#                  pyautogui.press("m")
#                  speak("video muted")
#                 # elif 'scroll' in command:
#                 #  speak("Activating gesture scroll detection.")
#                 #  import gesture  
#                 #  gesture.detect_gestures()

#                 # elif 'detect face' in command:
#                 #   speak("Activating face detection.")
#                 # import gesture
#                 #      gesture.detect_gestures()

#                 # elif 'object detection' in command:
#                 #      speak("Activating YOLO object detection.")
#                 # import gesture
#                 #     gesture.detect_gestures()
#                 elif "volume up" in query:
#                  from my_keyboard import volumeup
#                  speak("Turning volume up,sir")
#                  volumeup()
#                 elif "volume down" in query:
#                  from my_keyboard import volumedown
#                  speak("Turning volume down, sir")
#                  volumedown()

#                 elif "open" in query:
#                   from Dictapp import openappweb
#                   openappweb(query)
#                 elif "close" in query:
#                    from Dictapp import closeappweb
#                    closeappweb(query)

#                 elif "google" in query:
#                  from SearchNow import searchGoogle
#                  searchGoogle(query)
#                 elif "youtube" in query:
#                  from SearchNow import searchYoutube
#                  searchYoutube(query)
#                 elif "wikipedia" in query:
#                   from SearchNow import searchWikipedia
#                   searchWikipedia(query)
#                 # elif "temperature" in query:
#                 #  search = "temperature in delhi"
#                 #  url = f"https://www.google.com/search?q={search}"
#                 #  r  = requests.get(url)
#                 #  data = BeautifulSoup(r.text,"html.parser")
#                 #  temp = data.find("div", class_ = "BNeawe").text
#                 #  speak(f"current{search} is {temp}")
                
#                 # elif "weather" in query:
#                 #   search = "temperature in delhi"
#                 #   url = f"https://www.google.com/search?q={search}"
#                 #   r  = requests.get(url)
#                 #   data = BeautifulSoup(r.text,"html.parser")
#                 #   temp = data.find("div", class_ = "BNeawe").text
#                 #   speak(f"current{search} is {temp}") 
#                 elif "temperature" in query or "weather" in query:
#                     speak("Which city's weather do you want to know?")
#                     city_query = takeCommand()
#                     if city_query != "none":
#                         get_weather(city_query)  # Call function with user-specified city
#                     else:
#                         get_weather()  # Default to Delhi if no input
#                 elif "set an alarm" in query:
#                   print("input time example:- 10 and 10 and 10")
#                   speak("Set the time")
#                   a = input("Please tell the time :- ")
#                   alarm(a)
#                   speak("Done,sir")               
#                 elif "the time" in query:
#                     strTime = datetime.datetime.now().strftime("%H:%M")    
#                     speak(f"Sir, the time is {strTime}")
#                 elif "finally sleep" in query:
#                  speak("Going to sleep,sir")
#                  exit()
#                 elif "remember that" in query:
#                  rememberMessage = query.replace("remember that","")
#                  rememberMessage = query.replace("jarvis","")
#                  speak("You told me to remember that"+rememberMessage)
#                  remember = open("Remember.txt","a")
#                  remember.write(rememberMessage)
#                  remember.close()
#                 elif "what do you remember" in query:
#                  remember = open("Remember.txt","r")
#                  speak("You told me to remember that" + remember.read())
#                 elif "calculate" in query:
#                    from Calculatenumbers import WolfRamAlpha
#                    from Calculatenumbers import Calc
#                    query = query.replace("calculate","")
#                    query = query.replace("jarvis","")
#                    Calc(query)
#                 elif "screenshot" in query: 
#                    speak("Taking a screenshot now.")
#                    time.sleep(1)
#                    screenshot = pyautogui.screenshot()
#                    screenshot.save("screenshot.jpg")
#                    speak("Screenshot saved successfully.")
#                    print("Screenshot saved as screenshot.jpg")
#                 # elif "shutdown the system" in query:
#                 #  speak("Are You sure you want to shutdown")
#                 #  shutdown = input("Do you wish to shutdown your computer? (yes/no)")
#                 #  if shutdown == "yes":
#                 #      os.system("shutdown /s /t 1")

#                 # elif shutdown == "no":
#                 #  break


                
import pyttsx3
import speech_recognition
import requests
from bs4 import BeautifulSoup
import datetime
import pyautogui
import os
import my_keyboard
import random
import webbrowser
import NewsRead
import pywhatkit as kit
import time
import subprocess
import pyautogui
from INTRO import play_gif
play_gif()

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 300) 



def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def check_password():
    """Function to verify password before starting Jarvis"""
    try:
        with open("password.txt", "r") as pw_file:
            pw = pw_file.read().strip()  # Remove spaces/newlines
            print

        for i in range(3):  # Allow 3 attempts
            user_pw = input("Enter Password to open Jarvis: ").strip()

            if user_pw == pw:
                print("WELCOME SIR! PLZ SPEAK [WAKE UP] TO LOAD ME UP")
                return True
            elif i == 2:
                print("Too many incorrect attempts. Exiting...")
                exit()
            else:
                print("Incorrect Password. Try Again.")

    except FileNotFoundError:
        print("Error: password.txt not found. Please create the file.")
        exit()



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

# alarm set 
def alarm(query):
     timehere = open("Alarmtext.txt","a")
     timehere.write(query)
     timehere.close()
     os.startfile("alarm.py")
# weather report
def get_weather(city="Delhi"):  # Default city is Delhi
    api_key = "cf9b51d9e6eaa91fd1a10945e1c928d9"  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"

    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] == 200:  # ✅ Check if the request was successful
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        speak(f"The current temperature in {city} is {temp} degrees Celsius with {description}.")
    else:
        speak("Sorry, I couldn't fetch the weather details.")
# whatsapp automation
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

if __name__ == "__main__": 
     if check_password(): 
      while True:  
        query = takeCommand()
        # if face_login():  # Only activate Jarvis if face is recognized
        #  speak("Jarvis is ready to assist you.")
        if "wake up" in query:
            from GreetMe import greetMe
            greetMe()

            while True:
                query = takeCommand()

                if "go to sleep" in query:  # ✅ Fixed condition
                    speak("Ok sir, You can call me anytime")
                    print("Sleeping mode activated.")  
                    break  # Exits only after speaking    

                elif "click my photo" in query:
                        pyautogui.press("win")
                        time.sleep(1)
                        pyautogui.write("camera", interval=0.1)
                        time.sleep(1)
                        pyautogui.press("enter")
                        time.sleep(3)
                        speak("SMILE")
                        time.sleep(1)
                        pyautogui.press("enter")
                
                elif "hello" in query:
                    speak("Hello sir, how are you?")
                elif "i am fine" in query:
                    speak("That's great, sir")
                elif "how are you" in query:
                    speak("Perfect, sir")
                elif "thank you" in query:
                    speak("You're welcome, sir")
                elif "tired" in query:
                   speak("Playing your favourite songs, sir")
                   a = (1,2,3)
                   b = random.choice(a)
                   if b==1:
                    webbrowser.open("https://www.youtube.com/watch?v=TVbI55pDdaI")
                elif "news" in query:
                  from NewsRead import latestnews
                  latestnews()
                elif "send whatsapp" in query or "message on whatsapp" in query:
                 send_whatsapp_message_auto()
                
                elif "pause" in query:
                 pyautogui.press("k")
                 speak("video paused")
                elif "play" in query:
                 pyautogui.press("k")
                 speak("video played")
                elif "mute" in query:
                 pyautogui.press("m")
                 speak("video muted")

                elif "volume up" in query:
                 from my_keyboard import volumeup
                 speak("Turning volume up,sir")
                 volumeup()
                elif "volume down" in query:
                 from my_keyboard import volumedown
                 speak("Turning volume down, sir")
                 volumedown()

                elif "open" in query:
                  from Dictapp import openappweb
                  openappweb(query)
                elif "close" in query:
                   from Dictapp import closeappweb
                   closeappweb(query)

                elif "google" in query:
                 from SearchNow import searchGoogle
                 searchGoogle(query)
                elif "youtube" in query:
                 from SearchNow import searchYoutube
                 searchYoutube(query)
                elif "wikipedia" in query:
                  from SearchNow import searchWikipedia
                  searchWikipedia(query)
                # elif "temperature" in query:
                #  search = "temperature in delhi"
                #  url = f"https://www.google.com/search?q={search}"
                #  r  = requests.get(url)
                #  data = BeautifulSoup(r.text,"html.parser")
                #  temp = data.find("div", class_ = "BNeawe").text
                #  speak(f"current{search} is {temp}")
                
                # elif "weather" in query:
                #   search = "temperature in delhi"
                #   url = f"https://www.google.com/search?q={search}"
                #   r  = requests.get(url)
                #   data = BeautifulSoup(r.text,"html.parser")
                #   temp = data.find("div", class_ = "BNeawe").text
                #   speak(f"current{search} is {temp}") 
                elif "temperature" in query or "weather" in query:
                    speak("Which city's weather do you want to know?")
                    city_query = takeCommand()
                    if city_query != "none":
                        get_weather(city_query)  # Call function with user-specified city
                    else:
                        get_weather()  # Default to Delhi if no input
                elif "set an alarm" in query:
                  print("input time example:- 10 and 10 and 10")
                  speak("Set the time")
                  a = input("Please tell the time :- ")
                  alarm(a)
                  speak("Done,sir")               
                elif "the time" in query:
                    strTime = datetime.datetime.now().strftime("%H:%M")    
                    speak(f"Sir, the time is {strTime}")
                elif "finally sleep" in query:
                 speak("Going to sleep,sir")
                 exit()
                elif "remember that" in query:
                 rememberMessage = query.replace("remember that","")
                 rememberMessage = query.replace("jarvis","")
                 speak("You told me to remember that"+rememberMessage)
                 remember = open("Remember.txt","a")
                 remember.write(rememberMessage)
                 remember.close()
                elif "what do you remember" in query:
                 remember = open("Remember.txt","r")
                 speak("You told me to remember that" + remember.read())
                elif "calculate" in query:
                   from Calculatenumbers import WolfRamAlpha
                   from Calculatenumbers import Calc
                   query = query.replace("calculate","")
                   query = query.replace("jarvis","")
                   Calc(query)
                elif "screenshot" in query:  # <--- PASTE IT HERE
                   speak("Taking a screenshot now.")
                   time.sleep(1)
                   screenshot = pyautogui.screenshot()
                   screenshot.save("screenshot.jpg")
                   speak("Screenshot saved successfully.")
                   print("Screenshot saved as screenshot.jpg")