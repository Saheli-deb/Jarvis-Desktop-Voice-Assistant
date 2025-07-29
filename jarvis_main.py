             
import pyttsx3
from gesture_control import start_gesture_control
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
from dotenv import load_dotenv
from fpdf import FPDF
from scroll_control import scroll_up, scroll_down
from battery import check_battery
from generate_img import generate_image
from handle_system import handle_system_command
from youtube_automation import control_youtube
from handle_system import handle_system_command
from whatsapp_automation import send_whatsapp_message_auto
from pptx import Presentation
from pptx.util import Inches
from docx import Document
import os
import openai
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
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
def chat_with_gpt(prompt):
    system_role = "You are Jarvis, a smart, professional, and friendly desktop voice assistant created by Saheli. You can assist with any task, answer questions, or provide helpful information."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        reply = response['choices'][0]['message']['content']
        return reply.strip()
    except Exception as e:
        return "Sorry, I couldn't connect to ChatGPT at the moment."
def create_pdf(text, filename="chatbot_output.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(200, 10, txt=text)
    pdf.output(filename)
    speak(f"PDF saved as {filename}")

def create_word_doc(text, filename="chatbot_output.docx"):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(filename)
    speak(f"Word document saved as {filename}")

def create_ppt(text, filename="chatbot_output.pptx"):
    prs = Presentation()
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    title.text = "Jarvis Presentation"
    content.text = text
    prs.save(filename)
    speak(f"Presentation saved as {filename}")
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
                elif "shutdown" in query or "restart" in query or "log off" in query:
                  handle_system_command(query)
                elif "youtube automation" in query:
                    speak("What YouTube action should I perform?")
                    action = takeCommand()
                    control_youtube(action)
                elif "seek forward" in query:
                 control_youtube("seek forward")
                elif "seek backward" in query:
                    control_youtube("seek backward")
                elif "increase speed" in query:
                    control_youtube("increase speed")
                elif "decrease speed" in query:
                    control_youtube("decrease speed")

                elif "gesture control" in query or "enable gesture control" in query:
                        speak("Activating gesture control mode. Here's what you can do:")
                        print("""\n
                        ================= GESTURE CONTROL MENU =================
                        Finger Count |     Action
                        -------------|-----------------------
                            1        | Play / Pause
                            2        | Volume Up
                            3        | Volume Down
                            4        | Scroll Up
                            5        | Scroll Down
                        ========================================================
                        """)
                        start_gesture_control()
                        speak("Gesture control session ended.")

                elif "volume up" in query:
                 from my_keyboard import volumeup
                 speak("Turning volume up,sir")
                 volumeup()
                elif "volume down" in query:
                 from my_keyboard import volumedown
                 speak("Turning volume down, sir")
                 volumedown()
                elif "scroll up" in query:
                  speak("scrolling up sir")
                  scroll_up(20)

                elif "scroll down" in query:
                  speak("scrolling down sir")
                  scroll_down(20)

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
                elif "battery" in query or "charge" in query or "battery percentage" in query:
                     check_battery()
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
                elif "jarvis bot" in query or "chat bot" in query:
                  speak("Hello! I am your Jarvis ChatBot. Ask me anything.")
                  while True:
                     user_query = takeCommand()
                     if "exit chatbot" in user_query or "bye" in user_query:
                       speak("Exiting ChatBot mode. Back to main commands.")
                       break
                     elif user_query == "none":
                      continue
                    #  else:
                    #    response = chat_with_gpt(user_query)
                    #    print("Jarvis ChatBot:", response)
                    #    speak(response)
                     elif "make a pdf" in user_query or "create a pdf" in user_query:
                         if last_gpt_response:
                           create_pdf(last_gpt_response)
                         else:
                          speak("I don't have anything to save yet. Ask something first.")

                     elif "make a word" in user_query or "create word" in user_query:
                          if last_gpt_response:
                             create_word_doc(last_gpt_response)
                          else:
                              speak("I don't have anything to save yet. Ask something first.")

                     elif "make a ppt" in user_query or "create presentation" in user_query:
                          if last_gpt_response:
                           create_ppt(last_gpt_response)
                          else:
                           speak("I don't have anything to save yet. Ask something first.")
                     elif "generate content" in query:
                            speak("What content do you want me to generate?")
                            content_prompt = takeCommand()
                            result = chat_with_gpt(content_prompt)
                            print("Jarvis:", result)
                            speak(result)

                     else:
                        response = chat_with_gpt(user_query)
                        last_gpt_response = response  # Save for export
                        print("Jarvis ChatBot:", response)
                        speak(response)
                elif "generate image" in query or "make an image" in query:
                    speak("What image do you want me to generate?")
                    image_prompt = takeCommand()
                    generate_image(image_prompt)


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