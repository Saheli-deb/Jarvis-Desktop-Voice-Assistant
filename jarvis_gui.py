#!/usr/bin/env python3
"""
Jarvis GUI Frontend
Modern, sexy interface with red Jarvis theme
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
from datetime import datetime
import os
from PIL import Image, ImageTk
import json

class JarvisGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("JARVIS - Advanced AI Assistant")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0a0a0a')
        
        # Jarvis Red Theme Colors
        self.colors = {
            'bg_dark': '#0a0a0a',
            'bg_medium': '#1a1a1a',
            'bg_light': '#2a2a2a',
            'red_primary': '#ff0000',
            'red_secondary': '#cc0000',
            'red_accent': '#ff3333',
            'text_white': '#ffffff',
            'text_gray': '#cccccc',
            'text_dark': '#888888'
        }
        
        self.setup_gui()
        self.create_widgets()
        
    def setup_gui(self):
        """Setup the main GUI window"""
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Jarvis.TFrame', background=self.colors['bg_dark'])
        style.configure('Jarvis.TLabel', background=self.colors['bg_dark'], foreground=self.colors['text_white'])
        style.configure('Jarvis.TButton', 
                       background=self.colors['red_primary'],
                       foreground=self.colors['text_white'],
                       borderwidth=0,
                       focuscolor='none')
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, style='Jarvis.TFrame')
        main_frame.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)
        
        # Header
        self.create_header(main_frame)
        
        # Content area
        content_frame = ttk.Frame(main_frame, style='Jarvis.TFrame')
        content_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', pady=20)
        
        # Left sidebar
        self.create_sidebar(content_frame)
        
        # Main content area
        self.create_main_content(content_frame)
        
    def create_header(self, parent):
        """Create the header with Jarvis logo and status"""
        header_frame = ttk.Frame(parent, style='Jarvis.TFrame')
        header_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 20))
        
        # Jarvis Logo
        logo_label = tk.Label(header_frame, 
                             text="JARVIS", 
                             font=('Arial Black', 36, 'bold'),
                             fg=self.colors['red_primary'],
                             bg=self.colors['bg_dark'])
        logo_label.grid(row=0, column=0, sticky='w')
        
        # Subtitle
        subtitle_label = tk.Label(header_frame,
                                text="Advanced AI Assistant v2.0",
                                font=('Arial', 14),
                                fg=self.colors['text_gray'],
                                bg=self.colors['bg_dark'])
        subtitle_label.grid(row=1, column=0, sticky='w')
        
        # Status indicator
        self.status_label = tk.Label(header_frame,
                                   text="● READY",
                                   font=('Arial', 12, 'bold'),
                                   fg=self.colors['red_primary'],
                                   bg=self.colors['bg_dark'])
        self.status_label.grid(row=0, column=1, sticky='e', padx=(0, 20))
        
        # Time
        self.time_label = tk.Label(header_frame,
                                 text=datetime.now().strftime("%H:%M:%S"),
                                 font=('Arial', 12),
                                 fg=self.colors['text_gray'],
                                 bg=self.colors['bg_dark'])
        self.time_label.grid(row=1, column=1, sticky='e', padx=(0, 20))
        
        # Update time
        self.update_time()
        
    def create_sidebar(self, parent):
        """Create the left sidebar with feature categories"""
        sidebar_frame = ttk.Frame(parent, style='Jarvis.TFrame')
        sidebar_frame.grid(row=0, column=0, sticky='nsw', padx=(0, 20))
        
        # Sidebar title
        sidebar_title = tk.Label(sidebar_frame,
                               text="FEATURES",
                               font=('Arial Black', 16, 'bold'),
                               fg=self.colors['red_primary'],
                               bg=self.colors['bg_dark'])
        sidebar_title.grid(row=0, column=0, sticky='w', pady=(0, 20))
        
        # Feature categories
        categories = [
            ("🎭 AI PERSONALITY", "Switch between 5 AI personalities"),
            ("🤖 ENHANCED AI", "GPT-4, DALL-E 3, Whisper integration"),
            ("📊 ANALYTICS", "Track usage and performance"),
            ("🎮 VOICE GAMES", "Interactive games using voice"),
            ("🔧 ADVANCED", "File encryption, QR codes, scanning"),
            ("📋 REMINDERS", "Smart task management"),
            ("📧 EMAIL & CAL", "Email and calendar features"),
            ("🎵 MULTIMEDIA", "Photos, news, music"),
            ("🎮 MEDIA CTRL", "Video and audio control"),
            ("🖥️ SYSTEM", "System and app control"),
            ("🌐 WEB & SEARCH", "Web search and browsing"),
            ("🌤️ WEATHER", "Weather and time info"),
            ("🔋 SYSTEM INFO", "System information"),
            ("💬 CHAT", "Chatbot and memory")
        ]
        
        for i, (name, desc) in enumerate(categories, 1):
            # Category button
            btn = tk.Button(sidebar_frame,
                          text=f"{name}",
                          font=('Arial', 10, 'bold'),
                          fg=self.colors['text_white'],
                          bg=self.colors['bg_medium'],
                          activebackground=self.colors['red_primary'],
                          activeforeground=self.colors['text_white'],
                          relief='flat',
                          bd=0,
                          padx=15,
                          pady=8,
                          anchor='w',
                          width=20,
                          command=lambda cat=name: self.show_category(cat))
            btn.grid(row=i, column=0, sticky='ew', pady=2)
            
            # Hover effects
            btn.bind('<Enter>', lambda e, b=btn: b.configure(bg=self.colors['red_primary']))
            btn.bind('<Leave>', lambda e, b=btn: b.configure(bg=self.colors['bg_medium']))
            
    def create_main_content(self, parent):
        """Create the main content area"""
        content_frame = ttk.Frame(parent, style='Jarvis.TFrame')
        content_frame.grid(row=0, column=1, sticky='nsew')
        
        # Welcome message
        welcome_frame = tk.Frame(content_frame, bg=self.colors['bg_dark'])
        welcome_frame.grid(row=0, column=0, sticky='ew', pady=(0, 20))
        
        welcome_label = tk.Label(welcome_frame,
                               text="Welcome to JARVIS",
                               font=('Arial Black', 24, 'bold'),
                               fg=self.colors['red_primary'],
                               bg=self.colors['bg_dark'])
        welcome_label.grid(row=0, column=0, sticky='w')
        
        # Stats frame
        stats_frame = tk.Frame(content_frame, bg=self.colors['bg_medium'], relief='flat', bd=2)
        stats_frame.grid(row=1, column=0, sticky='ew', pady=(0, 20))
        
        # Statistics
        stats = [
            ("114+", "Voice Commands"),
            ("14", "Feature Categories"),
            ("5", "AI Personalities"),
            ("3", "Voice Games"),
            ("12+", "Advanced Features")
        ]
        
        for i, (value, label) in enumerate(stats):
            stat_frame = tk.Frame(stats_frame, bg=self.colors['bg_medium'])
            stat_frame.grid(row=0, column=i, padx=20, pady=15)
            
            value_label = tk.Label(stat_frame,
                                 text=value,
                                 font=('Arial Black', 20, 'bold'),
                                 fg=self.colors['red_primary'],
                                 bg=self.colors['bg_medium'])
            value_label.grid(row=0, column=0)
            
            desc_label = tk.Label(stat_frame,
                                text=label,
                                font=('Arial', 10),
                                fg=self.colors['text_gray'],
                                bg=self.colors['bg_medium'])
            desc_label.grid(row=1, column=0)
        
        # Quick commands frame
        commands_frame = tk.Frame(content_frame, bg=self.colors['bg_dark'])
        commands_frame.grid(row=2, column=0, sticky='ew', pady=(0, 20))
        
        commands_title = tk.Label(commands_frame,
                                text="Quick Commands",
                                font=('Arial Black', 16, 'bold'),
                                fg=self.colors['red_primary'],
                                bg=self.colors['bg_dark'])
        commands_title.grid(row=0, column=0, sticky='w', pady=(0, 15))
        
        # Quick command buttons
        quick_commands = [
            ("Jarvis, wake up", "Start Jarvis"),
            ("Jarvis, ai chat", "Advanced AI Chat"),
            ("Jarvis, switch personality", "Change AI Mode"),
            ("Jarvis, start trivia", "Play Trivia Game"),
            ("Jarvis, show my stats", "View Analytics"),
            ("Jarvis, generate ai image", "Create AI Image"),
            ("Jarvis, code help", "Programming Help"),
            ("Jarvis, go to sleep", "Stop Jarvis")
        ]
        
        for i, (command, desc) in enumerate(quick_commands):
            row = i // 2
            col = i % 2
            
            cmd_frame = tk.Frame(commands_frame, bg=self.colors['bg_medium'], relief='flat', bd=1)
            cmd_frame.grid(row=row+1, column=col, sticky='ew', padx=(0, 10), pady=5)
            
            cmd_label = tk.Label(cmd_frame,
                               text=command,
                               font=('Arial', 10, 'bold'),
                               fg=self.colors['text_white'],
                               bg=self.colors['bg_medium'])
            cmd_label.grid(row=0, column=0, sticky='w', padx=10, pady=5)
            
            desc_label = tk.Label(cmd_frame,
                                text=desc,
                                font=('Arial', 8),
                                fg=self.colors['text_gray'],
                                bg=self.colors['bg_medium'])
            desc_label.grid(row=1, column=0, sticky='w', padx=10, pady=(0, 5))
        
        # Console output
        console_frame = tk.Frame(content_frame, bg=self.colors['bg_dark'])
        console_frame.grid(row=3, column=0, sticky='ew')
        
        console_title = tk.Label(console_frame,
                               text="Console Output",
                               font=('Arial Black', 14, 'bold'),
                               fg=self.colors['red_primary'],
                               bg=self.colors['bg_dark'])
        console_title.grid(row=0, column=0, sticky='w', pady=(0, 10))
        
        # Console text area
        self.console_text = scrolledtext.ScrolledText(console_frame,
                                                    width=80,
                                                    height=10,
                                                    bg=self.colors['bg_medium'],
                                                    fg=self.colors['text_white'],
                                                    font=('Consolas', 10),
                                                    relief='flat',
                                                    bd=0)
        self.console_text.grid(row=1, column=0, sticky='ew')
        
        # Add initial message
        self.log_message("JARVIS GUI initialized successfully!")
        self.log_message("Ready to assist you with 114+ voice commands.")
        
    def show_category(self, category):
        """Show details for a specific category"""
        self.log_message(f"Selected category: {category}")
        
        # Update status
        self.status_label.config(text="● BROWSE")
        
        # Category-specific commands
        commands_map = {
            "🎭 AI PERSONALITY": [
                "Jarvis, switch personality",
                "Jarvis, personality info",
                "Jarvis, list personalities",
                "Jarvis, switch ai context",
                "Jarvis, change ai mode"
            ],
            "🤖 ENHANCED AI": [
                "Jarvis, ai chat",
                "Jarvis, generate ai image",
                "Jarvis, analyze sentiment",
                "Jarvis, translate",
                "Jarvis, summarize",
                "Jarvis, code help",
                "Jarvis, smart reminder",
                "Jarvis, ai research",
                "Jarvis, ai status",
                "Jarvis, text to speech"
            ],
            "📊 ANALYTICS": [
                "Jarvis, show my stats",
                "Jarvis, usage statistics",
                "Jarvis, system performance report"
            ],
            "🎮 VOICE GAMES": [
                "Jarvis, start trivia",
                "Jarvis, start word game",
                "Jarvis, start story",
                "Jarvis, game status"
            ],
            "🔧 ADVANCED": [
                "Jarvis, system monitor",
                "Jarvis, encrypt file",
                "Jarvis, generate qr code",
                "Jarvis, generate password",
                "Jarvis, organize files",
                "Jarvis, scan network"
            ]
        }
        
        if category in commands_map:
            self.log_message(f"Available commands for {category}:")
            for cmd in commands_map[category]:
                self.log_message(f"  • {cmd}")
        
    def log_message(self, message):
        """Add a message to the console"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.console_text.see(tk.END)
        
    def update_time(self):
        """Update the time display"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
        
    def run(self):
        """Start the GUI"""
        self.root.mainloop()

def main():
    """Main function to start the GUI"""
    app = JarvisGUI()
    app.run()

if __name__ == "__main__":
    main() 