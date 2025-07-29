import customtkinter as ctk
import threading
import jarvis_main
import tkinter.simpledialog
import tkinter.messagebox
import pyautogui
import time
import random
import webbrowser
import datetime
from PIL import Image, ImageTk, ImageSequence
import os
from jarvis_main import speak
from jarvis_main import chat_with_gpt

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

FEATURES = [
    "Chat",
    "Weather",
    "Alarm",
    "Screenshot",
    "YouTube",
    "Gesture",
    "Battery",
    "WhatsApp",
    "Generate Image",
    "Export (PDF/Word/PPT)"
]

# --- Password Dialog ---
def password_dialog():
    root = ctk.CTk()
    root.withdraw()
    for _ in range(3):
        pw = tkinter.simpledialog.askstring("Password", "Enter Password to open Jarvis:", show='*')
        if pw is None:
            root.destroy()
            exit()
        try:
            with open("password.txt", "r") as pw_file:
                correct_pw = pw_file.read().strip()
        except FileNotFoundError:
            tkinter.messagebox.showerror("Error", "password.txt not found. Please create the file.")
            root.destroy()
            exit()
        if pw == correct_pw:
            root.destroy()
            return True
        else:
            tkinter.messagebox.showerror("Incorrect", "Incorrect Password. Try Again.")
    tkinter.messagebox.showerror("Error", "Too many incorrect attempts. Exiting...")
    root.destroy()
    exit()

# --- Command Routing (from main loop) ---
def process_full_command(query, last_gpt_response=None):
    from jarvis_main import speak, chat_with_gpt, check_battery, handle_system_command, control_youtube, start_gesture_control, generate_image, alarm, get_weather, send_whatsapp_message_auto
    # This is a simplified version of your main loop logic, adapted for UI use
    response = None
    query = query.lower()
    if "wake up" in query:
        from GreetMe import greetMe
        greetMe()
        return "Jarvis is ready to assist you.", None
    elif "go to sleep" in query:
        speak("Ok sir, You can call me anytime")
        return "Sleeping mode activated.", None
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
        return "Photo clicked!", None
    elif "hello" in query:
        speak("Hello sir, how are you?")
        return "Hello sir, how are you?", None
    elif "i am fine" in query:
        speak("That's great, sir")
        return "That's great, sir", None
    elif "how are you" in query:
        speak("Perfect, sir")
        return "Perfect, sir", None
    elif "thank you" in query:
        speak("You're welcome, sir")
        return "You're welcome, sir", None
    elif "tired" in query:
        speak("Playing your favourite songs, sir")
        a = (1,2,3)
        b = random.choice(a)
        if b==1:
            webbrowser.open("https://www.youtube.com/watch?v=TVbI55pDdaI")
        return "Playing your favourite songs, sir", None
    elif "news" in query:
        from NewsRead import latestnews
        latestnews()
        return "Reading latest news...", None
    elif "send whatsapp" in query or "message on whatsapp" in query:
        send_whatsapp_message_auto()
        return "WhatsApp message sent (if details provided).", None
    elif "pause" in query:
        pyautogui.press("k")
        speak("video paused")
        return "Video paused", None
    elif "play" in query:
        pyautogui.press("k")
        speak("video played")
        return "Video played", None
    elif "mute" in query:
        pyautogui.press("m")
        speak("video muted")
        return "Video muted", None
    elif "shutdown" in query or "restart" in query or "log off" in query:
        handle_system_command(query)
        return "System command executed.", None
    elif "youtube automation" in query:
        speak("What YouTube action should I perform?")
        # In UI, user should use YouTube panel for specific actions
        return "Please use the YouTube panel for specific actions.", None
    elif "seek forward" in query:
        control_youtube("seek forward")
        return "YouTube seek forward.", None
    elif "seek backward" in query:
        control_youtube("seek backward")
        return "YouTube seek backward.", None
    elif "increase speed" in query:
        control_youtube("increase speed")
        return "YouTube speed increased.", None
    elif "decrease speed" in query:
        control_youtube("decrease speed")
        return "YouTube speed decreased.", None
    elif "gesture control" in query or "enable gesture control" in query:
        speak("Activating gesture control mode. Here's what you can do:")
        start_gesture_control()
        speak("Gesture control session ended.")
        return "Gesture control session ended.", None
    elif "volume up" in query:
        from my_keyboard import volumeup
        speak("Turning volume up,sir")
        volumeup()
        return "Volume up.", None
    elif "volume down" in query:
        from my_keyboard import volumedown
        speak("Turning volume down, sir")
        volumedown()
        return "Volume down.", None
    elif "scroll up" in query:
        speak("scrolling up sir")
        scroll_up(20)
        return "Scrolled up.", None
    elif "scroll down" in query:
        speak("scrolling down sir")
        scroll_down(20)
        return "Scrolled down.", None
    elif "open" in query:
        from Dictapp import openappweb
        openappweb(query)
        return "App/web opened.", None
    elif "close" in query:
        from Dictapp import closeappweb
        closeappweb(query)
        return "App/web closed.", None
    elif "google" in query:
        from SearchNow import searchGoogle
        searchGoogle(query)
        return "Google search done.", None
    elif "youtube" in query:
        from SearchNow import searchYoutube
        searchYoutube(query)
        return "YouTube search done.", None
    elif "wikipedia" in query:
        from SearchNow import searchWikipedia
        searchWikipedia(query)
        return "Wikipedia search done.", None
    elif "temperature" in query or "weather" in query:
        speak("Which city's weather do you want to know?")
        # In UI, user should use Weather panel for city input
        return "Please use the Weather panel for city input.", None
    elif "battery" in query or "charge" in query or "battery percentage" in query:
        check_battery()
        return "Battery status spoken aloud.", None
    elif "set an alarm" in query:
        speak("Set the time")
        # In UI, user should use Alarm panel for time input
        return "Please use the Alarm panel to set the time.", None
    elif "the time" in query:
        strTime = datetime.datetime.now().strftime("%H:%M")
        speak(f"Sir, the time is {strTime}")
        return f"Sir, the time is {strTime}", None
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
        return "Remembered.", None
    elif "what do you remember" in query:
        remember = open("Remember.txt","r")
        msg = remember.read()
        speak("You told me to remember that" + msg)
        return f"You told me to remember that {msg}", None
    elif "jarvis bot" in query or "chat bot" in query:
        speak("Hello! I am your Jarvis ChatBot. Ask me anything.")
        return "ChatBot mode: Ask me anything! (Type 'exit chatbot' to leave)", None
    elif "generate image" in query or "make an image" in query:
        speak("What image do you want me to generate?")
        # In UI, user should use Generate Image panel
        return "Please use the Generate Image panel.", None
    elif "calculate" in query:
        from Calculatenumbers import WolfRamAlpha
        from Calculatenumbers import Calc
        query = query.replace("calculate","")
        query = query.replace("jarvis","")
        Calc(query)
        return "Calculation done.", None
    elif "screenshot" in query:
        speak("Taking a screenshot now.")
        time.sleep(1)
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.jpg")
        speak("Screenshot saved successfully.")
        return "Screenshot saved as screenshot.jpg", None
    else:
        # Default: ChatGPT
        response = chat_with_gpt(query)
        return response, response

# --- Jarvis Theme Colors ---
JARVIS_BG = "#181c23"
JARVIS_PANEL = "#23272e"
JARVIS_SIDEBAR = "#1a222d"
JARVIS_HIGHLIGHT = "#00e6ff"
JARVIS_ACCENT = "#00bfff"
JARVIS_TEXT = "#e6f7ff"
JARVIS_CONSOLE = "#10131a"
JARVIS_BORDER = "#00e6ff"
JARVIS_BTN_HOVER = "#003d4d"
JARVIS_BTN_ACTIVE = "#00bfff"
JARVIS_TITLE_FONT = ("Segoe UI", 26, "bold")
JARVIS_LABEL_FONT = ("Consolas", 15, "bold")
JARVIS_BTN_FONT = ("Segoe UI", 14, "bold")
JARVIS_CONSOLE_FONT = ("Consolas", 13)

class JarvisUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("JARVIS - Professional Desktop Assistant")
        self.geometry("950x650")
        self.resizable(False, False)
        self.configure(bg=JARVIS_BG)
        self.selected_feature = ctk.StringVar(value="Chat")
        self.last_gpt_response = ""
        self.gif_frames = []
        self.gif_label = None
        self.gif_index = 0
        self.create_widgets()

    def create_widgets(self):
        # Remove Sidebar, add Menu Bar
        self.menu_bar = ctk.CTkFrame(self, height=50, fg_color=JARVIS_SIDEBAR, border_width=2, border_color=JARVIS_HIGHLIGHT)
        self.menu_bar.pack(side="top", fill="x")
        self.menu_bar.pack_propagate(False)

        # Add feature buttons to menu bar
        for feat in FEATURES:
            btn = ctk.CTkButton(
                self.menu_bar, text=feat, width=110, height=38, font=JARVIS_BTN_FONT,
                fg_color=JARVIS_PANEL, text_color=JARVIS_TEXT, hover_color=JARVIS_BTN_HOVER,
                border_width=2, border_color=JARVIS_ACCENT, corner_radius=12,
                command=lambda f=feat: self.show_panel(f)
            )
            btn.pack(side="left", padx=6, pady=6)

        # Main content area
        self.main_area = ctk.CTkFrame(self, fg_color=JARVIS_PANEL, border_width=2, border_color=JARVIS_HIGHLIGHT, corner_radius=18)
        self.main_area.pack(side="top", fill="both", expand=True, padx=18, pady=(0,18))
        self.panels = {}
        self.create_panels()
        self.status_label = ctk.CTkLabel(self, text="Ready", font=("Segoe UI", 13), text_color=JARVIS_ACCENT)
        self.status_label.pack(side="bottom", fill="x", pady=(0, 2))
        self.show_panel("Chat")

    def create_panels(self):
        # Chat panel
        chat_panel = ctk.CTkFrame(self.main_area, fg_color=JARVIS_PANEL, corner_radius=16)
        chat_panel.pack_propagate(False)
        chat_panel.place(relwidth=1, relheight=1)
        ctk.CTkLabel(chat_panel, text="JARVIS Console", font=JARVIS_LABEL_FONT, text_color=JARVIS_HIGHLIGHT).pack(pady=(18, 0))
        self.chat_conversation = ctk.CTkTextbox(
            chat_panel, width=700, height=350, font=JARVIS_CONSOLE_FONT,
            fg_color=JARVIS_CONSOLE, text_color=JARVIS_TEXT, border_width=2, border_color=JARVIS_ACCENT, corner_radius=10
        )
        self.chat_conversation.pack(pady=12)
        self.chat_conversation.configure(state="disabled")
        chat_input_frame = ctk.CTkFrame(chat_panel, fg_color=JARVIS_PANEL)
        chat_input_frame.pack(pady=10)
        self.chat_input_box = ctk.CTkEntry(
            chat_input_frame, width=420, font=JARVIS_CONSOLE_FONT, fg_color=JARVIS_CONSOLE, text_color=JARVIS_TEXT,
            border_width=2, border_color=JARVIS_ACCENT, corner_radius=8, placeholder_text="Type your command here..."
        )
        self.chat_input_box.pack(side="left", padx=(0, 10), pady=10)
        self.chat_input_box.bind("<Return>", lambda event: self.send_chat_command())
        self.chat_send_btn = ctk.CTkButton(
            chat_input_frame, text="Send", width=90, font=JARVIS_BTN_FONT,
            fg_color=JARVIS_HIGHLIGHT, text_color=JARVIS_BG, hover_color=JARVIS_BTN_ACTIVE, corner_radius=8,
            command=self.send_chat_command
        )
        self.chat_send_btn.pack(side="left", padx=(0, 10))
        self.chat_speak_btn = ctk.CTkButton(
            chat_input_frame, text="Speak 🎤", width=90, font=JARVIS_BTN_FONT,
            fg_color=JARVIS_ACCENT, text_color=JARVIS_BG, hover_color=JARVIS_BTN_ACTIVE, corner_radius=8,
            command=self.speak_chat_command
        )
        self.chat_speak_btn.pack(side="left")
        self.panels["Chat"] = chat_panel

        # Weather panel
        weather_panel = ctk.CTkFrame(self.main_area, fg_color=JARVIS_PANEL, corner_radius=16)
        weather_panel.pack_propagate(False)
        ctk.CTkLabel(weather_panel, text="Weather Report", font=JARVIS_LABEL_FONT, text_color=JARVIS_HIGHLIGHT).pack(pady=20)
        self.weather_city_entry = ctk.CTkEntry(weather_panel, width=320, font=JARVIS_CONSOLE_FONT, fg_color=JARVIS_CONSOLE, text_color=JARVIS_TEXT, border_width=2, border_color=JARVIS_ACCENT, corner_radius=8, placeholder_text="Enter city name...")
        self.weather_city_entry.pack(pady=10)
        ctk.CTkButton(weather_panel, text="Get Weather", font=JARVIS_BTN_FONT, fg_color=JARVIS_HIGHLIGHT, text_color=JARVIS_BG, hover_color=JARVIS_BTN_ACTIVE, corner_radius=8, command=self.get_weather).pack(pady=10)
        self.weather_result = ctk.CTkLabel(weather_panel, text="", font=JARVIS_CONSOLE_FONT, text_color=JARVIS_TEXT)
        self.weather_result.pack(pady=10)
        self.panels["Weather"] = weather_panel

        # Alarm panel
        alarm_panel = ctk.CTkFrame(self.main_area, fg_color=JARVIS_PANEL, corner_radius=16)
        alarm_panel.pack_propagate(False)
        ctk.CTkLabel(alarm_panel, text="Set Alarm", font=JARVIS_LABEL_FONT, text_color=JARVIS_HIGHLIGHT).pack(pady=20)
        self.alarm_time_entry = ctk.CTkEntry(alarm_panel, width=220, font=JARVIS_CONSOLE_FONT, fg_color=JARVIS_CONSOLE, text_color=JARVIS_TEXT, border_width=2, border_color=JARVIS_ACCENT, corner_radius=8, placeholder_text="HH:MM:SS")
        self.alarm_time_entry.pack(pady=10)
        ctk.CTkButton(alarm_panel, text="Set Alarm", font=JARVIS_BTN_FONT, fg_color=JARVIS_HIGHLIGHT, text_color=JARVIS_BG, hover_color=JARVIS_BTN_ACTIVE, corner_radius=8, command=self.set_alarm).pack(pady=10)
        self.panels["Alarm"] = alarm_panel

        # Screenshot panel
        screenshot_panel = ctk.CTkFrame(self.main_area, fg_color=JARVIS_PANEL, corner_radius=16)
        screenshot_panel.pack_propagate(False)
        ctk.CTkLabel(screenshot_panel, text="Screenshot", font=JARVIS_LABEL_FONT, text_color=JARVIS_HIGHLIGHT).pack(pady=20)
        ctk.CTkButton(screenshot_panel, text="Take Screenshot", font=JARVIS_BTN_FONT, fg_color=JARVIS_HIGHLIGHT, text_color=JARVIS_BG, hover_color=JARVIS_BTN_ACTIVE, corner_radius=8, command=self.take_screenshot).pack(pady=10)
        self.panels["Screenshot"] = screenshot_panel

        # YouTube panel
        yt_panel = ctk.CTkFrame(self.main_area, fg_color=JARVIS_PANEL, corner_radius=16)
        yt_panel.pack_propagate(False)
        ctk.CTkLabel(yt_panel, text="YouTube Automation", font=JARVIS_LABEL_FONT, text_color=JARVIS_HIGHLIGHT).pack(pady=20)
        yt_btns = [
            ("Play/Pause", lambda: self.youtube_action("play")),
            ("Mute", lambda: self.youtube_action("mute")),
            ("Seek Forward", lambda: self.youtube_action("seek forward")),
            ("Seek Backward", lambda: self.youtube_action("seek backward")),
            ("Increase Speed", lambda: self.youtube_action("increase speed")),
            ("Decrease Speed", lambda: self.youtube_action("decrease speed")),
        ]
        for txt, cmd in yt_btns:
            ctk.CTkButton(yt_panel, text=txt, font=JARVIS_BTN_FONT, fg_color=JARVIS_HIGHLIGHT, text_color=JARVIS_BG, hover_color=JARVIS_BTN_HOVER, corner_radius=8, command=cmd).pack(pady=5)
        self.panels["YouTube"] = yt_panel

        # Gesture panel
        gesture_panel = ctk.CTkFrame(self.main_area, fg_color=JARVIS_PANEL, corner_radius=16)
        gesture_panel.pack_propagate(False)
        ctk.CTkLabel(gesture_panel, text="Gesture Control", font=JARVIS_LABEL_FONT, text_color=JARVIS_HIGHLIGHT).pack(pady=20)
        ctk.CTkButton(gesture_panel, text="Start Gesture Control", font=JARVIS_BTN_FONT, fg_color=JARVIS_HIGHLIGHT, text_color=JARVIS_BG, hover_color=JARVIS_BTN_ACTIVE, corner_radius=8, command=self.start_gesture).pack(pady=10)
        self.panels["Gesture"] = gesture_panel

        # Battery panel
        battery_panel = ctk.CTkFrame(self.main_area, fg_color=JARVIS_PANEL, corner_radius=16)
        battery_panel.pack_propagate(False)
        ctk.CTkLabel(battery_panel, text="Battery Status", font=JARVIS_LABEL_FONT, text_color=JARVIS_HIGHLIGHT).pack(pady=20)
        ctk.CTkButton(battery_panel, text="Check Battery", font=JARVIS_BTN_FONT, fg_color=JARVIS_HIGHLIGHT, text_color=JARVIS_BG, hover_color=JARVIS_BTN_ACTIVE, corner_radius=8, command=self.check_battery).pack(pady=10)
        self.panels["Battery"] = battery_panel

        # WhatsApp panel
        wa_panel = ctk.CTkFrame(self.main_area, fg_color=JARVIS_PANEL, corner_radius=16)
        wa_panel.pack_propagate(False)
        ctk.CTkLabel(wa_panel, text="WhatsApp Automation", font=JARVIS_LABEL_FONT, text_color=JARVIS_HIGHLIGHT).pack(pady=20)
        ctk.CTkButton(wa_panel, text="Send WhatsApp Message", font=JARVIS_BTN_FONT, fg_color=JARVIS_HIGHLIGHT, text_color=JARVIS_BG, hover_color=JARVIS_BTN_ACTIVE, corner_radius=8, command=self.send_whatsapp).pack(pady=10)
        self.panels["WhatsApp"] = wa_panel

        # Generate Image panel
        img_panel = ctk.CTkFrame(self.main_area, fg_color=JARVIS_PANEL, corner_radius=16)
        img_panel.pack_propagate(False)
        ctk.CTkLabel(img_panel, text="Generate Image", font=JARVIS_LABEL_FONT, text_color=JARVIS_HIGHLIGHT).pack(pady=20)
        self.img_prompt_entry = ctk.CTkEntry(img_panel, width=420, font=JARVIS_CONSOLE_FONT, fg_color=JARVIS_CONSOLE, text_color=JARVIS_TEXT, border_width=2, border_color=JARVIS_ACCENT, corner_radius=8, placeholder_text="Describe the image...")
        self.img_prompt_entry.pack(pady=10)
        ctk.CTkButton(img_panel, text="Generate", font=JARVIS_BTN_FONT, fg_color=JARVIS_HIGHLIGHT, text_color=JARVIS_BG, hover_color=JARVIS_BTN_ACTIVE, corner_radius=8, command=self.generate_image).pack(pady=10)
        self.panels["Generate Image"] = img_panel

        # Export panel
        export_panel = ctk.CTkFrame(self.main_area, fg_color=JARVIS_PANEL, corner_radius=16)
        export_panel.pack_propagate(False)
        ctk.CTkLabel(export_panel, text="Export Last Chat Response", font=JARVIS_LABEL_FONT, text_color=JARVIS_HIGHLIGHT).pack(pady=20)
        ctk.CTkButton(export_panel, text="Export as PDF", font=JARVIS_BTN_FONT, fg_color=JARVIS_HIGHLIGHT, text_color=JARVIS_BG, hover_color=JARVIS_BTN_ACTIVE, corner_radius=8, command=self.export_pdf).pack(pady=10)
        ctk.CTkButton(export_panel, text="Export as Word", font=JARVIS_BTN_FONT, fg_color=JARVIS_HIGHLIGHT, text_color=JARVIS_BG, hover_color=JARVIS_BTN_ACTIVE, corner_radius=8, command=self.export_word).pack(pady=10)
        ctk.CTkButton(export_panel, text="Export as PPT", font=JARVIS_BTN_FONT, fg_color=JARVIS_HIGHLIGHT, text_color=JARVIS_BG, hover_color=JARVIS_BTN_ACTIVE, corner_radius=8, command=self.export_ppt).pack(pady=10)
        self.panels["Export (PDF/Word/PPT)"] = export_panel

        # Email panel
        email_panel = ctk.CTkFrame(self.main_area, fg_color=JARVIS_PANEL, corner_radius=16)
        email_panel.pack_propagate(False)
        ctk.CTkLabel(email_panel, text="Email Assistant", font=JARVIS_LABEL_FONT, text_color=JARVIS_HIGHLIGHT).pack(pady=20)
        self.email_recipient_entry = ctk.CTkEntry(email_panel, width=320, font=JARVIS_CONSOLE_FONT, fg_color=JARVIS_CONSOLE, text_color=JARVIS_TEXT, border_width=2, border_color=JARVIS_ACCENT, corner_radius=8, placeholder_text="Recipient Email")
        self.email_recipient_entry.pack(pady=5)
        self.email_subject_entry = ctk.CTkEntry(email_panel, width=320, font=JARVIS_CONSOLE_FONT, fg_color=JARVIS_CONSOLE, text_color=JARVIS_TEXT, border_width=2, border_color=JARVIS_ACCENT, corner_radius=8, placeholder_text="Subject")
        self.email_subject_entry.pack(pady=5)
        self.email_body_entry = ctk.CTkTextbox(email_panel, width=320, height=80, font=JARVIS_CONSOLE_FONT, fg_color=JARVIS_CONSOLE, text_color=JARVIS_TEXT, border_width=2, border_color=JARVIS_ACCENT, corner_radius=8)
        self.email_body_entry.pack(pady=5)
        ctk.CTkButton(email_panel, text="Send Email", font=JARVIS_BTN_FONT, fg_color=JARVIS_HIGHLIGHT, text_color=JARVIS_BG, hover_color=JARVIS_BTN_ACTIVE, corner_radius=8, command=self.send_email_ui).pack(pady=10)
        ctk.CTkButton(email_panel, text="Read Latest Emails", font=JARVIS_BTN_FONT, fg_color=JARVIS_HIGHLIGHT, text_color=JARVIS_BG, hover_color=JARVIS_BTN_ACTIVE, corner_radius=8, command=self.read_emails_ui).pack(pady=5)
        self.email_result = ctk.CTkLabel(email_panel, text="", font=JARVIS_CONSOLE_FONT, text_color=JARVIS_TEXT)
        self.email_result.pack(pady=10)
        self.panels["Email"] = email_panel

        # Calendar panel
        calendar_panel = ctk.CTkFrame(self.main_area, fg_color=JARVIS_PANEL, corner_radius=16)
        calendar_panel.pack_propagate(False)
        ctk.CTkLabel(calendar_panel, text="Calendar Assistant", font=JARVIS_LABEL_FONT, text_color=JARVIS_HIGHLIGHT).pack(pady=20)
        self.calendar_title_entry = ctk.CTkEntry(calendar_panel, width=320, font=JARVIS_CONSOLE_FONT, fg_color=JARVIS_CONSOLE, text_color=JARVIS_TEXT, border_width=2, border_color=JARVIS_ACCENT, corner_radius=8, placeholder_text="Event Title")
        self.calendar_title_entry.pack(pady=5)
        self.calendar_date_entry = ctk.CTkEntry(calendar_panel, width=320, font=JARVIS_CONSOLE_FONT, fg_color=JARVIS_CONSOLE, text_color=JARVIS_TEXT, border_width=2, border_color=JARVIS_ACCENT, corner_radius=8, placeholder_text="Date (MM/DD/YYYY)")
        self.calendar_date_entry.pack(pady=5)
        self.calendar_time_entry = ctk.CTkEntry(calendar_panel, width=320, font=JARVIS_CONSOLE_FONT, fg_color=JARVIS_CONSOLE, text_color=JARVIS_TEXT, border_width=2, border_color=JARVIS_ACCENT, corner_radius=8, placeholder_text="Time (HH:MM) or leave empty for all day")
        self.calendar_time_entry.pack(pady=5)
        self.calendar_desc_entry = ctk.CTkTextbox(calendar_panel, width=320, height=60, font=JARVIS_CONSOLE_FONT, fg_color=JARVIS_CONSOLE, text_color=JARVIS_TEXT, border_width=2, border_color=JARVIS_ACCENT, corner_radius=8)
        self.calendar_desc_entry.pack(pady=5)
        ctk.CTkButton(calendar_panel, text="Add Event", font=JARVIS_BTN_FONT, fg_color=JARVIS_HIGHLIGHT, text_color=JARVIS_BG, hover_color=JARVIS_BTN_ACTIVE, corner_radius=8, command=self.add_calendar_event).pack(pady=10)
        ctk.CTkButton(calendar_panel, text="List Upcoming Events", font=JARVIS_BTN_FONT, fg_color=JARVIS_HIGHLIGHT, text_color=JARVIS_BG, hover_color=JARVIS_BTN_ACTIVE, corner_radius=8, command=self.list_calendar_events).pack(pady=5)
        ctk.CTkButton(calendar_panel, text="Today's Events", font=JARVIS_BTN_FONT, fg_color=JARVIS_HIGHLIGHT, text_color=JARVIS_BG, hover_color=JARVIS_BTN_ACTIVE, corner_radius=8, command=self.get_today_events).pack(pady=5)
        ctk.CTkButton(calendar_panel, text="Open System Calendar", font=JARVIS_BTN_FONT, fg_color=JARVIS_ACCENT, text_color=JARVIS_BG, hover_color=JARVIS_BTN_ACTIVE, corner_radius=8, command=self.open_system_calendar).pack(pady=5)
        ctk.CTkButton(calendar_panel, text="Open Google Calendar", font=JARVIS_BTN_FONT, fg_color=JARVIS_ACCENT, text_color=JARVIS_BG, hover_color=JARVIS_BTN_ACTIVE, corner_radius=8, command=self.open_google_calendar).pack(pady=5)
        ctk.CTkButton(calendar_panel, text="Add to Google Calendar", font=JARVIS_BTN_FONT, fg_color=JARVIS_ACCENT, text_color=JARVIS_BG, hover_color=JARVIS_BTN_ACTIVE, corner_radius=8, command=self.add_to_google_calendar).pack(pady=5)
        self.calendar_result = ctk.CTkLabel(calendar_panel, text="", font=JARVIS_CONSOLE_FONT, text_color=JARVIS_TEXT)
        self.calendar_result.pack(pady=10)
        self.panels["Calendar"] = calendar_panel

        # Reminders & Todos panel
        reminders_panel = ctk.CTkFrame(self.main_area, fg_color=JARVIS_PANEL, corner_radius=16)
        reminders_panel.pack_propagate(False)
        ctk.CTkLabel(reminders_panel, text="Reminders & Todos", font=JARVIS_LABEL_FONT, text_color=JARVIS_HIGHLIGHT).pack(pady=20)
        
        # Reminder fields
        ctk.CTkLabel(reminders_panel, text="Add Reminder:", font=JARVIS_CONSOLE_FONT, text_color=JARVIS_ACCENT).pack(pady=(0,5))
        self.reminder_title_entry = ctk.CTkEntry(reminders_panel, width=320, font=JARVIS_CONSOLE_FONT, fg_color=JARVIS_CONSOLE, text_color=JARVIS_TEXT, border_width=2, border_color=JARVIS_ACCENT, corner_radius=8, placeholder_text="Reminder Title")
        self.reminder_title_entry.pack(pady=2)
        self.reminder_date_entry = ctk.CTkEntry(reminders_panel, width=320, font=JARVIS_CONSOLE_FONT, fg_color=JARVIS_CONSOLE, text_color=JARVIS_TEXT, border_width=2, border_color=JARVIS_ACCENT, corner_radius=8, placeholder_text="Due Date (MM/DD/YYYY) - optional")
        self.reminder_date_entry.pack(pady=2)
        self.reminder_priority_entry = ctk.CTkEntry(reminders_panel, width=320, font=JARVIS_CONSOLE_FONT, fg_color=JARVIS_CONSOLE, text_color=JARVIS_TEXT, border_width=2, border_color=JARVIS_ACCENT, corner_radius=8, placeholder_text="Priority (high/medium/low) - default: medium")
        self.reminder_priority_entry.pack(pady=2)
        self.reminder_desc_entry = ctk.CTkTextbox(reminders_panel, width=320, height=40, font=JARVIS_CONSOLE_FONT, fg_color=JARVIS_CONSOLE, text_color=JARVIS_TEXT, border_width=2, border_color=JARVIS_ACCENT, corner_radius=8)
        self.reminder_desc_entry.pack(pady=2)
        ctk.CTkButton(reminders_panel, text="Add Reminder", font=JARVIS_BTN_FONT, fg_color=JARVIS_HIGHLIGHT, text_color=JARVIS_BG, hover_color=JARVIS_BTN_ACTIVE, corner_radius=8, command=self.add_reminder).pack(pady=5)
        
        # Todo fields
        ctk.CTkLabel(reminders_panel, text="Add Todo:", font=JARVIS_CONSOLE_FONT, text_color=JARVIS_ACCENT).pack(pady=(10,5))
        self.todo_title_entry = ctk.CTkEntry(reminders_panel, width=320, font=JARVIS_CONSOLE_FONT, fg_color=JARVIS_CONSOLE, text_color=JARVIS_TEXT, border_width=2, border_color=JARVIS_ACCENT, corner_radius=8, placeholder_text="Todo Title")
        self.todo_title_entry.pack(pady=2)
        self.todo_date_entry = ctk.CTkEntry(reminders_panel, width=320, font=JARVIS_CONSOLE_FONT, fg_color=JARVIS_CONSOLE, text_color=JARVIS_TEXT, border_width=2, border_color=JARVIS_ACCENT, corner_radius=8, placeholder_text="Due Date (MM/DD/YYYY) - optional")
        self.todo_date_entry.pack(pady=2)
        self.todo_priority_entry = ctk.CTkEntry(reminders_panel, width=320, font=JARVIS_CONSOLE_FONT, fg_color=JARVIS_CONSOLE, text_color=JARVIS_TEXT, border_width=2, border_color=JARVIS_ACCENT, corner_radius=8, placeholder_text="Priority (high/medium/low) - default: medium")
        self.todo_priority_entry.pack(pady=2)
        self.todo_desc_entry = ctk.CTkTextbox(reminders_panel, width=320, height=40, font=JARVIS_CONSOLE_FONT, fg_color=JARVIS_CONSOLE, text_color=JARVIS_TEXT, border_width=2, border_color=JARVIS_ACCENT, corner_radius=8)
        self.todo_desc_entry.pack(pady=2)
        ctk.CTkButton(reminders_panel, text="Add Todo", font=JARVIS_BTN_FONT, fg_color=JARVIS_HIGHLIGHT, text_color=JARVIS_BG, hover_color=JARVIS_BTN_ACTIVE, corner_radius=8, command=self.add_todo).pack(pady=5)
        
        # Action buttons
        ctk.CTkButton(reminders_panel, text="List Reminders", font=JARVIS_BTN_FONT, fg_color=JARVIS_ACCENT, text_color=JARVIS_BG, hover_color=JARVIS_BTN_ACTIVE, corner_radius=8, command=self.list_reminders).pack(pady=5)
        ctk.CTkButton(reminders_panel, text="List Todos", font=JARVIS_BTN_FONT, fg_color=JARVIS_ACCENT, text_color=JARVIS_BG, hover_color=JARVIS_BTN_ACTIVE, corner_radius=8, command=self.list_todos).pack(pady=5)
        ctk.CTkButton(reminders_panel, text="Check Overdue", font=JARVIS_BTN_FONT, fg_color=JARVIS_ACCENT, text_color=JARVIS_BG, hover_color=JARVIS_BTN_ACTIVE, corner_radius=8, command=self.check_overdue).pack(pady=5)
        ctk.CTkButton(reminders_panel, text="Test Notification", font=JARVIS_BTN_FONT, fg_color=JARVIS_ACCENT, text_color=JARVIS_BG, hover_color=JARVIS_BTN_ACTIVE, corner_radius=8, command=self.test_notification).pack(pady=5)
        
        self.reminders_result = ctk.CTkLabel(reminders_panel, text="", font=JARVIS_CONSOLE_FONT, text_color=JARVIS_TEXT)
        self.reminders_result.pack(pady=10)
        self.panels["Reminders & Todos"] = reminders_panel

    def show_panel(self, feature):
        for f, panel in self.panels.items():
            panel.place_forget()
        self.panels[feature].place(relwidth=1, relheight=1)
        self.selected_feature.set(feature)
        self.set_status(f"{feature} ready.")

    # --- Chat/Command logic ---
    def send_chat_command(self):
        user_input = self.chat_input_box.get().strip()
        if not user_input:
            return
        self.append_chat(f"You: {user_input}")
        self.chat_input_box.delete(0, ctk.END)
        self.set_status("Processing...")
        threading.Thread(target=self.process_chat_command, args=(user_input, False), daemon=True).start()

    def speak_chat_command(self):
        self.append_chat("You (voice): ...")
        self.set_status("Listening...")
        threading.Thread(target=self.process_chat_command, args=("", True), daemon=True).start()

    def process_chat_command(self, user_input, use_voice):
        if use_voice:
            query = jarvis_main.takeCommand()
        else:
            query = user_input
        if query and query.strip().lower() != "none":
            response, self.last_gpt_response = process_full_command(query, self.last_gpt_response)
        else:
            response = "Sorry, I didn't catch that."
        self.append_chat(f"Jarvis: {response}")
        self.set_status("Ready")

    def append_chat(self, text):
        self.chat_conversation.configure(state="normal")
        self.chat_conversation.insert("end", text + "\n")
        self.chat_conversation.see("end")
        self.chat_conversation.configure(state="disabled")

    # --- Weather logic ---
    def get_weather(self):
        city = self.weather_city_entry.get().strip()
        if not city:
            self.weather_result.configure(text="Please enter a city name.")
            return
        self.set_status("Fetching weather...")
        def fetch():
            jarvis_main.get_weather(city)
            self.weather_result.configure(text=f"Weather for {city} spoken aloud.")
            self.set_status("Ready")
        threading.Thread(target=fetch, daemon=True).start()

    # --- Alarm logic ---
    def set_alarm(self):
        time_str = self.alarm_time_entry.get().strip()
        if not time_str:
            self.set_status("Please enter a time (HH:MM:SS).")
            return
        self.set_status("Setting alarm...")
        def set_alarm_thread():
            jarvis_main.alarm(time_str)
            self.set_status("Alarm set!")
        threading.Thread(target=set_alarm_thread, daemon=True).start()

    # --- Screenshot logic ---
    def take_screenshot(self):
        self.set_status("Taking screenshot...")
        def screenshot_thread():
            import time
            time.sleep(1)
            screenshot = jarvis_main.pyautogui.screenshot()
            screenshot.save("screenshot.jpg")
            self.set_status("Screenshot saved as screenshot.jpg.")
        threading.Thread(target=screenshot_thread, daemon=True).start()

    # --- YouTube logic ---
    def youtube_action(self, action):
        self.set_status(f"Performing YouTube action: {action}")
        def yt_thread():
            jarvis_main.control_youtube(action)
            self.set_status(f"YouTube action '{action}' done.")
        threading.Thread(target=yt_thread, daemon=True).start()

    # --- Gesture logic ---
    def start_gesture(self):
        self.set_status("Starting gesture control...")
        def gesture_thread():
            jarvis_main.start_gesture_control()
            self.set_status("Gesture control session ended.")
        threading.Thread(target=gesture_thread, daemon=True).start()

    # --- Battery logic ---
    def check_battery(self):
        self.set_status("Checking battery...")
        def battery_thread():
            jarvis_main.check_battery()
            self.set_status("Battery status spoken aloud.")
        threading.Thread(target=battery_thread, daemon=True).start()

    # --- WhatsApp logic ---
    def send_whatsapp(self):
        self.set_status("Sending WhatsApp message...")
        def wa_thread():
            jarvis_main.send_whatsapp_message_auto()
            self.set_status("WhatsApp message sent (if details provided).")
        threading.Thread(target=wa_thread, daemon=True).start()

    # --- Generate Image logic ---
    def generate_image(self):
        prompt = self.img_prompt_entry.get().strip()
        if not prompt:
            self.set_status("Please enter an image description.")
            return
        self.set_status("Generating image...")
        def img_thread():
            jarvis_main.generate_image(prompt)
            self.set_status("Image generated and saved.")
        threading.Thread(target=img_thread, daemon=True).start()

    # --- Export logic ---
    def export_pdf(self):
        if not self.last_gpt_response:
            self.set_status("No chat response to export.")
            return
        self.set_status("Exporting as PDF...")
        def pdf_thread():
            jarvis_main.create_pdf(self.last_gpt_response)
            self.set_status("PDF exported.")
        threading.Thread(target=pdf_thread, daemon=True).start()

    def export_word(self):
        if not self.last_gpt_response:
            self.set_status("No chat response to export.")
            return
        self.set_status("Exporting as Word...")
        def word_thread():
            jarvis_main.create_word_doc(self.last_gpt_response)
            self.set_status("Word document exported.")
        threading.Thread(target=word_thread, daemon=True).start()

    def export_ppt(self):
        if not self.last_gpt_response:
            self.set_status("No chat response to export.")
            return
        self.set_status("Exporting as PPT...")
        def ppt_thread():
            jarvis_main.create_ppt(self.last_gpt_response)
            self.set_status("PPT exported.")
        threading.Thread(target=ppt_thread, daemon=True).start()

    def send_email_ui(self):
        import email_assistant
        recipient = self.email_recipient_entry.get().strip()
        subject = self.email_subject_entry.get().strip()
        body = self.email_body_entry.get("1.0", "end").strip()
        if not recipient or not subject or not body:
            self.email_result.configure(text="Please fill all fields.")
            return
        self.set_status("Sending email...")
        success = email_assistant.send_email(recipient, subject, body)
        if success:
            self.email_result.configure(text=f"Email sent to {recipient}.")
        else:
            self.email_result.configure(text="Failed to send email. Check setup.")
        self.set_status("Ready")

    def read_emails_ui(self):
        import email_assistant
        self.set_status("Fetching emails...")
        emails = email_assistant.read_emails()
        if not emails:
            self.email_result.configure(text="No emails found or failed to fetch emails.")
        else:
            result = ""
            for mail in emails:
                result += f"From: {mail['from']}\nSubject: {mail['subject']}\n{mail['body'][:100]}\n---\n"
            self.email_result.configure(text=result)
        self.set_status("Ready")

    def add_calendar_event(self):
        import calendar_assistant
        title = self.calendar_title_entry.get().strip()
        date = self.calendar_date_entry.get().strip()
        time = self.calendar_time_entry.get().strip()
        description = self.calendar_desc_entry.get("1.0", "end").strip()
        
        if not title or not date:
            self.calendar_result.configure(text="Please fill title and date.")
            return
            
        self.set_status("Adding calendar event...")
        success = calendar_assistant.add_event(title, date, time, description)
        if success:
            self.calendar_result.configure(text=f"Event '{title}' added successfully!")
            # Clear fields
            self.calendar_title_entry.delete(0, ctk.END)
            self.calendar_date_entry.delete(0, ctk.END)
            self.calendar_time_entry.delete(0, ctk.END)
            self.calendar_desc_entry.delete("1.0", "end")
        else:
            self.calendar_result.configure(text="Failed to add event. Check date format (MM/DD/YYYY).")
        self.set_status("Ready")

    def list_calendar_events(self):
        import calendar_assistant
        self.set_status("Fetching calendar events...")
        events = calendar_assistant.list_events()
        if events:
            result = f"Found {len(events)} upcoming events:\n\n"
            for event in events:
                from datetime import datetime
                event_date = datetime.fromisoformat(event['datetime'])
                result += f"📌 {event['title']}\n"
                result += f"   📅 {event_date.strftime('%B %d, %Y at %I:%M %p')}\n"
                if event['description']:
                    result += f"   📝 {event['description']}\n"
                result += "---\n"
        else:
            result = "No upcoming events found."
        self.calendar_result.configure(text=result)
        self.set_status("Ready")

    def get_today_events(self):
        import calendar_assistant
        self.set_status("Checking today's events...")
        today_events = calendar_assistant.get_today_events()
        if today_events:
            result = f"You have {len(today_events)} events today:\n\n"
            for event in today_events:
                from datetime import datetime
                event_date = datetime.fromisoformat(event['datetime'])
                result += f"📌 {event['title']}\n"
                result += f"   📅 {event_date.strftime('%I:%M %p')}\n"
                if event['description']:
                    result += f"   📝 {event['description']}\n"
                result += "---\n"
        else:
            result = "No events scheduled for today."
        self.calendar_result.configure(text=result)
        self.set_status("Ready")

    def open_system_calendar(self):
        import calendar_assistant
        self.set_status("Opening system calendar...")
        success = calendar_assistant.open_system_calendar()
        if success:
            self.calendar_result.configure(text="✅ System calendar opened!")
        else:
            self.calendar_result.configure(text="❌ Failed to open system calendar.")
        self.set_status("Ready")

    def open_google_calendar(self):
        import calendar_assistant
        self.set_status("Opening Google Calendar...")
        success = calendar_assistant.open_google_calendar()
        if success:
            self.calendar_result.configure(text="✅ Google Calendar opened in browser!")
        else:
            self.calendar_result.configure(text="❌ Failed to open Google Calendar.")
        self.set_status("Ready")

    def add_to_google_calendar(self):
        import calendar_assistant
        title = self.calendar_title_entry.get().strip()
        date = self.calendar_date_entry.get().strip()
        time = self.calendar_time_entry.get().strip()
        description = self.calendar_desc_entry.get("1.0", "end").strip()
        
        if not title or not date:
            self.calendar_result.configure(text="Please fill title and date first.")
            return
            
        self.set_status("Opening Google Calendar with event...")
        success = calendar_assistant.open_calendar_with_event(title, date, time, description)
        if success:
            self.calendar_result.configure(text=f"✅ Google Calendar opened with event: {title}")
        else:
            self.calendar_result.configure(text="❌ Failed to open Google Calendar with event.")
        self.set_status("Ready")

    def add_reminder(self):
        import reminders_assistant
        title = self.reminder_title_entry.get().strip()
        due_date = self.reminder_date_entry.get().strip()
        priority = self.reminder_priority_entry.get().strip() or "medium"
        description = self.reminder_desc_entry.get("1.0", "end").strip()
        
        if not title:
            self.reminders_result.configure(text="Please fill the reminder title.")
            return
            
        self.set_status("Adding reminder...")
        success = reminders_assistant.add_reminder(title, due_date, priority, description)
        if success:
            self.reminders_result.configure(text=f"✅ Reminder '{title}' added successfully!")
            # Clear fields
            self.reminder_title_entry.delete(0, ctk.END)
            self.reminder_date_entry.delete(0, ctk.END)
            self.reminder_priority_entry.delete(0, ctk.END)
            self.reminder_desc_entry.delete("1.0", "end")
        else:
            self.reminders_result.configure(text="❌ Failed to add reminder. Check date format (MM/DD/YYYY).")
        self.set_status("Ready")

    def add_todo(self):
        import reminders_assistant
        title = self.todo_title_entry.get().strip()
        due_date = self.todo_date_entry.get().strip()
        priority = self.todo_priority_entry.get().strip() or "medium"
        description = self.todo_desc_entry.get("1.0", "end").strip()
        
        if not title:
            self.reminders_result.configure(text="Please fill the todo title.")
            return
            
        self.set_status("Adding todo...")
        success = reminders_assistant.add_todo(title, priority, description, due_date)
        if success:
            self.reminders_result.configure(text=f"✅ Todo '{title}' added successfully!")
            # Clear fields
            self.todo_title_entry.delete(0, ctk.END)
            self.todo_date_entry.delete(0, ctk.END)
            self.todo_priority_entry.delete(0, ctk.END)
            self.todo_desc_entry.delete("1.0", "end")
        else:
            self.reminders_result.configure(text="❌ Failed to add todo.")
        self.set_status("Ready")

    def list_reminders(self):
        import reminders_assistant
        self.set_status("Fetching reminders...")
        reminders = reminders_assistant.list_reminders()
        if reminders:
            result = f"Found {len(reminders)} active reminders:\n\n"
            for reminder in reminders:
                result += f"⏰ {reminder['title']}\n"
                result += f"   ⚡ Priority: {reminder['priority']}\n"
                if reminder['due_date']:
                    from datetime import datetime
                    due_date = datetime.fromisoformat(reminder['due_date'])
                    result += f"   📅 Due: {due_date.strftime('%B %d, %Y')}\n"
                if reminder['description']:
                    result += f"   📝 {reminder['description']}\n"
                result += "---\n"
        else:
            result = "No active reminders found."
        self.reminders_result.configure(text=result)
        self.set_status("Ready")

    def list_todos(self):
        import reminders_assistant
        self.set_status("Fetching todos...")
        todos = reminders_assistant.list_todos()
        if todos:
            result = f"Found {len(todos)} active todos:\n\n"
            for todo in todos:
                result += f"⏳ {todo['title']}\n"
                result += f"   ⚡ Priority: {todo['priority']}\n"
                if todo['description']:
                    result += f"   📝 {todo['description']}\n"
                result += "---\n"
        else:
            result = "No active todos found."
        self.reminders_result.configure(text=result)
        self.set_status("Ready")

    def check_overdue(self):
        import reminders_assistant
        self.set_status("Checking overdue reminders...")
        overdue = reminders_assistant.get_overdue_reminders()
        if overdue:
            result = f"Found {len(overdue)} overdue reminders:\n\n"
            for reminder in overdue:
                result += f"🔴 OVERDUE: {reminder['title']}\n"
                if reminder['due_date']:
                    from datetime import datetime
                    due_date = datetime.fromisoformat(reminder['due_date'])
                    result += f"   📅 Was due: {due_date.strftime('%B %d, %Y')}\n"
                result += "---\n"
        else:
            result = "No overdue reminders found."
        self.reminders_result.configure(text=result)
        self.set_status("Ready")

    def test_notification(self):
        import reminders_assistant
        self.set_status("Testing notification...")
        reminders_assistant.test_notification()
        self.reminders_result.configure(text="✅ Test notification sent! Check your desktop.")
        self.set_status("Ready")

    def set_status(self, text):
        self.status_label.configure(text=text)

    def load_gif(self, gif_path):
        # Load all frames of the GIF as CTkImage
        gif = Image.open(gif_path)
        self.gif_frames = [ctk.CTkImage(light_image=frame.copy().convert('RGBA'), size=frame.size) for frame in ImageSequence.Iterator(gif)]
        self.gif_index = 0

    def animate_gif(self):
        if self.gif_frames and self.gif_label:
            try:
                frame = self.gif_frames[self.gif_index]
                self.gif_label.configure(image=frame)
                self.gif_label.image = frame  # Prevent garbage collection
                self.gif_index = (self.gif_index + 1) % len(self.gif_frames)
                self.after(60, self.animate_gif)  # Adjust speed as needed
            except Exception:
                pass  # Widget might be destroyed during shutdown

if __name__ == "__main__":
    password_dialog() # Call the password dialog at startup
    app = JarvisUI()
    app.mainloop() 