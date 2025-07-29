#!/usr/bin/env python3
"""
Advanced Jarvis GUI Frontend
Sexy interface with animations, particle effects, and red Jarvis theme
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import random
import math
from datetime import datetime
import os
from PIL import Image, ImageTk
import json

class Particle:
    """Particle for background animation"""
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.life = random.randint(50, 150)
        self.max_life = self.life
        self.size = random.randint(1, 3)
        self.id = canvas.create_oval(x, y, x+self.size, y+self.size, 
                                   fill='#ff0000', outline='#ff3333', width=0)
    
    def update(self):
        """Update particle position and life"""
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        
        # Bounce off edges
        if self.x <= 0 or self.x >= self.canvas.winfo_width():
            self.vx *= -1
        if self.y <= 0 or self.y >= self.canvas.winfo_height():
            self.vy *= -1
        
        # Update visual
        alpha = self.life / self.max_life
        color = f'#{int(255*alpha):02x}0000'
        self.canvas.coords(self.id, self.x, self.y, self.x+self.size, self.y+self.size)
        self.canvas.itemconfig(self.id, fill=color)
        
        return self.life > 0

class JarvisAdvancedGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("JARVIS - Advanced AI Assistant v2.0")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0a0a0a')
        
        # Make window fullscreen optional
        self.root.attributes('-zoomed', True)
        
        # Jarvis Red Theme Colors
        self.colors = {
            'bg_dark': '#0a0a0a',
            'bg_medium': '#1a1a1a',
            'bg_light': '#2a2a2a',
            'red_primary': '#ff0000',
            'red_secondary': '#cc0000',
            'red_accent': '#ff3333',
            'red_glow': '#ff6666',
            'text_white': '#ffffff',
            'text_gray': '#cccccc',
            'text_dark': '#888888'
        }
        
        # Animation variables
        self.particles = []
        self.animation_running = True
        
        self.setup_gui()
        self.create_widgets()
        self.start_animations()
        
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
        # Background canvas for particles
        self.bg_canvas = tk.Canvas(self.root, bg=self.colors['bg_dark'], 
                                  highlightthickness=0)
        self.bg_canvas.grid(row=0, column=0, columnspan=2, rowspan=2, sticky='nsew')
        
        # Main container
        main_frame = ttk.Frame(self.root, style='Jarvis.TFrame')
        main_frame.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=20, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Content area
        content_frame = ttk.Frame(main_frame, style='Jarvis.TFrame')
        content_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', pady=20)
        
        # Left sidebar
        self.create_sidebar(content_frame)
        
        # Main content area
        self.create_main_content(content_frame)
        
        # Status bar
        self.create_status_bar()
        
    def create_header(self, parent):
        """Create the animated header with Jarvis logo"""
        header_frame = ttk.Frame(parent, style='Jarvis.TFrame')
        header_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 20))
        
        # Animated Jarvis Logo
        self.logo_label = tk.Label(header_frame, 
                                  text="JARVIS", 
                                  font=('Arial Black', 48, 'bold'),
                                  fg=self.colors['red_primary'],
                                  bg=self.colors['bg_dark'])
        self.logo_label.grid(row=0, column=0, sticky='w')
        
        # Glowing effect for logo
        self.animate_logo()
        
        # Subtitle with typewriter effect
        self.subtitle_label = tk.Label(header_frame,
                                     text="",
                                     font=('Arial', 16),
                                     fg=self.colors['text_gray'],
                                     bg=self.colors['bg_dark'])
        self.subtitle_label.grid(row=1, column=0, sticky='w')
        
        # Typewriter effect for subtitle
        self.typewriter_text("Advanced AI Assistant v2.0", self.subtitle_label)
        
        # Status indicator with animation
        self.status_label = tk.Label(header_frame,
                                   text="● READY",
                                   font=('Arial', 14, 'bold'),
                                   fg=self.colors['red_primary'],
                                   bg=self.colors['bg_dark'])
        self.status_label.grid(row=0, column=1, sticky='e', padx=(0, 20))
        
        # Time with glow effect
        self.time_label = tk.Label(header_frame,
                                 text=datetime.now().strftime("%H:%M:%S"),
                                 font=('Arial', 14),
                                 fg=self.colors['red_glow'],
                                 bg=self.colors['bg_dark'])
        self.time_label.grid(row=1, column=1, sticky='e', padx=(0, 20))
        
        # Update time
        self.update_time()
        
    def create_sidebar(self, parent):
        """Create the animated left sidebar"""
        sidebar_frame = ttk.Frame(parent, style='Jarvis.TFrame')
        sidebar_frame.grid(row=0, column=0, sticky='nsw', padx=(0, 20))
        
        # Sidebar title with glow
        sidebar_title = tk.Label(sidebar_frame,
                               text="FEATURES",
                               font=('Arial Black', 18, 'bold'),
                               fg=self.colors['red_primary'],
                               bg=self.colors['bg_dark'])
        sidebar_title.grid(row=0, column=0, sticky='w', pady=(0, 20))
        
        # Feature categories with hover effects
        categories = [
            ("🎭 AI PERSONALITY", "Switch between 5 AI personalities", self.colors['red_primary']),
            ("🤖 ENHANCED AI", "GPT-4, DALL-E 3, Whisper integration", self.colors['red_accent']),
            ("📊 ANALYTICS", "Track usage and performance", self.colors['red_secondary']),
            ("🎮 VOICE GAMES", "Interactive games using voice", self.colors['red_primary']),
            ("🔧 ADVANCED", "File encryption, QR codes, scanning", self.colors['red_accent']),
            ("📋 REMINDERS", "Smart task management", self.colors['red_secondary']),
            ("📧 EMAIL & CAL", "Email and calendar features", self.colors['red_primary']),
            ("🎵 MULTIMEDIA", "Photos, news, music", self.colors['red_accent']),
            ("🎮 MEDIA CTRL", "Video and audio control", self.colors['red_secondary']),
            ("🖥️ SYSTEM", "System and app control", self.colors['red_primary']),
            ("🌐 WEB & SEARCH", "Web search and browsing", self.colors['red_accent']),
            ("🌤️ WEATHER", "Weather and time info", self.colors['red_secondary']),
            ("🔋 SYSTEM INFO", "System information", self.colors['red_primary']),
            ("💬 CHAT", "Chatbot and memory", self.colors['red_accent'])
        ]
        
        self.category_buttons = []
        for i, (name, desc, color) in enumerate(categories, 1):
            # Category button with glow effect
            btn = tk.Button(sidebar_frame,
                          text=f"{name}",
                          font=('Arial', 11, 'bold'),
                          fg=self.colors['text_white'],
                          bg=self.colors['bg_medium'],
                          activebackground=color,
                          activeforeground=self.colors['text_white'],
                          relief='flat',
                          bd=0,
                          padx=20,
                          pady=10,
                          anchor='w',
                          width=22,
                          command=lambda cat=name: self.show_category(cat))
            btn.grid(row=i, column=0, sticky='ew', pady=3)
            
            # Enhanced hover effects
            btn.bind('<Enter>', lambda e, b=btn, c=color: self.on_button_hover(b, c))
            btn.bind('<Leave>', lambda e, b=btn: self.on_button_leave(b))
            
            self.category_buttons.append(btn)
            
    def create_main_content(self, parent):
        """Create the main content area with animations"""
        content_frame = ttk.Frame(parent, style='Jarvis.TFrame')
        content_frame.grid(row=0, column=1, sticky='nsew')
        
        # Welcome message with fade-in effect
        welcome_frame = tk.Frame(content_frame, bg=self.colors['bg_dark'])
        welcome_frame.grid(row=0, column=0, sticky='ew', pady=(0, 20))
        
        self.welcome_label = tk.Label(welcome_frame,
                                    text="Welcome to JARVIS",
                                    font=('Arial Black', 28, 'bold'),
                                    fg=self.colors['red_primary'],
                                    bg=self.colors['bg_dark'])
        self.welcome_label.grid(row=0, column=0, sticky='w')
        
        # Animated stats frame
        stats_frame = tk.Frame(content_frame, bg=self.colors['bg_medium'], 
                              relief='flat', bd=2)
        stats_frame.grid(row=1, column=0, sticky='ew', pady=(0, 20))
        
        # Statistics with counting animation
        stats = [
            ("114+", "Voice Commands"),
            ("14", "Feature Categories"),
            ("5", "AI Personalities"),
            ("3", "Voice Games"),
            ("12+", "Advanced Features")
        ]
        
        self.stat_labels = []
        for i, (value, label) in enumerate(stats):
            stat_frame = tk.Frame(stats_frame, bg=self.colors['bg_medium'])
            stat_frame.grid(row=0, column=i, padx=25, pady=20)
            
            value_label = tk.Label(stat_frame,
                                 text="0",
                                 font=('Arial Black', 24, 'bold'),
                                 fg=self.colors['red_primary'],
                                 bg=self.colors['bg_medium'])
            value_label.grid(row=0, column=0)
            
            desc_label = tk.Label(stat_frame,
                                text=label,
                                font=('Arial', 11),
                                fg=self.colors['text_gray'],
                                bg=self.colors['bg_medium'])
            desc_label.grid(row=1, column=0)
            
            self.stat_labels.append((value_label, value))
        
        # Animate stats counting
        self.animate_stats()
        
        # Quick commands with hover effects
        commands_frame = tk.Frame(content_frame, bg=self.colors['bg_dark'])
        commands_frame.grid(row=2, column=0, sticky='ew', pady=(0, 20))
        
        commands_title = tk.Label(commands_frame,
                                text="Quick Commands",
                                font=('Arial Black', 18, 'bold'),
                                fg=self.colors['red_primary'],
                                bg=self.colors['bg_dark'])
        commands_title.grid(row=0, column=0, sticky='w', pady=(0, 15))
        
        # Quick command buttons with animations
        quick_commands = [
            ("Jarvis, wake up", "Start Jarvis", "🚀"),
            ("Jarvis, ai chat", "Advanced AI Chat", "🤖"),
            ("Jarvis, switch personality", "Change AI Mode", "🎭"),
            ("Jarvis, start trivia", "Play Trivia Game", "🎮"),
            ("Jarvis, show my stats", "View Analytics", "📊"),
            ("Jarvis, generate ai image", "Create AI Image", "🎨"),
            ("Jarvis, code help", "Programming Help", "💻"),
            ("Jarvis, go to sleep", "Stop Jarvis", "😴")
        ]
        
        for i, (command, desc, icon) in enumerate(quick_commands):
            row = i // 2
            col = i % 2
            
            cmd_frame = tk.Frame(commands_frame, bg=self.colors['bg_medium'], 
                                relief='flat', bd=1)
            cmd_frame.grid(row=row+1, column=col, sticky='ew', padx=(0, 15), pady=8)
            
            # Icon
            icon_label = tk.Label(cmd_frame,
                                text=icon,
                                font=('Arial', 16),
                                fg=self.colors['red_primary'],
                                bg=self.colors['bg_medium'])
            icon_label.grid(row=0, column=0, padx=(10, 5), pady=5)
            
            # Command text
            cmd_label = tk.Label(cmd_frame,
                               text=command,
                               font=('Arial', 10, 'bold'),
                               fg=self.colors['text_white'],
                               bg=self.colors['bg_medium'])
            cmd_label.grid(row=0, column=1, sticky='w', pady=5)
            
            desc_label = tk.Label(cmd_frame,
                                text=desc,
                                font=('Arial', 8),
                                fg=self.colors['text_gray'],
                                bg=self.colors['bg_medium'])
            desc_label.grid(row=1, column=1, sticky='w', pady=(0, 5))
            
            # Hover effects
            cmd_frame.bind('<Enter>', lambda e, f=cmd_frame: f.configure(bg=self.colors['red_primary']))
            cmd_frame.bind('<Leave>', lambda e, f=cmd_frame: f.configure(bg=self.colors['bg_medium']))
        
        # Console output with typing effect
        console_frame = tk.Frame(content_frame, bg=self.colors['bg_dark'])
        console_frame.grid(row=3, column=0, sticky='ew')
        
        console_title = tk.Label(console_frame,
                               text="Console Output",
                               font=('Arial Black', 16, 'bold'),
                               fg=self.colors['red_primary'],
                               bg=self.colors['bg_dark'])
        console_title.grid(row=0, column=0, sticky='w', pady=(0, 10))
        
        # Console text area with syntax highlighting
        self.console_text = scrolledtext.ScrolledText(console_frame,
                                                    width=90,
                                                    height=12,
                                                    bg=self.colors['bg_medium'],
                                                    fg=self.colors['text_white'],
                                                    font=('Consolas', 10),
                                                    relief='flat',
                                                    bd=0,
                                                    insertbackground=self.colors['red_primary'])
        self.console_text.grid(row=1, column=0, sticky='ew')
        
        # Add initial messages with typing effect
        self.type_console_message("JARVIS GUI initialized successfully!")
        self.type_console_message("Ready to assist you with 114+ voice commands.")
        self.type_console_message("All systems operational.")
        
    def create_status_bar(self):
        """Create animated status bar"""
        status_frame = tk.Frame(self.root, bg=self.colors['bg_medium'], height=30)
        status_frame.grid(row=1, column=0, columnspan=2, sticky='ew')
        status_frame.grid_propagate(False)
        
        # Status text
        self.status_text = tk.Label(status_frame,
                                  text="JARVIS v2.0 - Advanced AI Assistant",
                                  font=('Arial', 10),
                                  fg=self.colors['text_gray'],
                                  bg=self.colors['bg_medium'])
        self.status_text.grid(row=0, column=0, sticky='w', padx=10, pady=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, 
                                           variable=self.progress_var,
                                           length=200,
                                           mode='determinate')
        self.progress_bar.grid(row=0, column=1, sticky='e', padx=10, pady=5)
        
        # Animate progress bar
        self.animate_progress()
        
    def animate_logo(self):
        """Animate the Jarvis logo with glow effect"""
        colors = [self.colors['red_primary'], self.colors['red_accent'], 
                 self.colors['red_glow'], self.colors['red_secondary']]
        current_color = colors[0]
        
        def cycle_colors():
            nonlocal current_color
            current_index = colors.index(current_color)
            current_color = colors[(current_index + 1) % len(colors)]
            self.logo_label.configure(fg=current_color)
            if self.animation_running:
                self.root.after(1000, cycle_colors)
        
        cycle_colors()
        
    def typewriter_text(self, text, label, index=0):
        """Typewriter effect for text"""
        if index < len(text):
            label.configure(text=text[:index+1])
            self.root.after(50, lambda: self.typewriter_text(text, label, index+1))
            
    def type_console_message(self, message):
        """Add message to console with typing effect"""
        def type_message(index=0):
            if index < len(message):
                self.console_text.insert(tk.END, message[index])
                self.console_text.see(tk.END)
                self.root.after(20, lambda: type_message(index+1))
            else:
                self.console_text.insert(tk.END, "\n")
                self.console_text.see(tk.END)
        
        self.root.after(1000, type_message)
        
    def animate_stats(self):
        """Animate statistics counting up"""
        for label, target in self.stat_labels:
            target_value = int(target.replace('+', ''))
            current = int(label.cget('text') or 0)
            
            if current < target_value:
                label.configure(text=str(current + 1))
                self.root.after(50, lambda: self.animate_stats())
                break
                
    def animate_progress(self):
        """Animate progress bar"""
        current = self.progress_var.get()
        if current < 100:
            self.progress_var.set(current + 1)
            self.root.after(50, self.animate_progress)
            
    def on_button_hover(self, button, color):
        """Enhanced hover effect for buttons"""
        button.configure(bg=color)
        button.configure(font=('Arial', 11, 'bold'))
        
    def on_button_leave(self, button):
        """Reset button on leave"""
        button.configure(bg=self.colors['bg_medium'])
        button.configure(font=('Arial', 11, 'bold'))
        
    def show_category(self, category):
        """Show details for a specific category with animation"""
        self.log_message(f"Selected category: {category}")
        
        # Update status with animation
        self.status_label.config(text="● BROWSE")
        self.animate_status()
        
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
                
    def animate_status(self):
        """Animate status indicator"""
        statuses = ["● READY", "● BROWSE", "● ACTIVE", "● READY"]
        current = self.status_label.cget('text')
        next_status = statuses[(statuses.index(current) + 1) % len(statuses)]
        self.status_label.config(text=next_status)
        
    def log_message(self, message):
        """Add a message to the console with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.console_text.see(tk.END)
        
    def update_time(self):
        """Update the time display"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
        
    def start_animations(self):
        """Start particle animations"""
        def animate_particles():
            # Create new particles
            if len(self.particles) < 20:
                x = random.randint(0, self.bg_canvas.winfo_width())
                y = random.randint(0, self.bg_canvas.winfo_height())
                self.particles.append(Particle(self.bg_canvas, x, y))
            
            # Update existing particles
            for particle in self.particles[:]:
                if not particle.update():
                    self.bg_canvas.delete(particle.id)
                    self.particles.remove(particle)
            
            if self.animation_running:
                self.root.after(50, animate_particles)
        
        animate_particles()
        
    def run(self):
        """Start the GUI"""
        self.root.mainloop()
        self.animation_running = False

def main():
    """Main function to start the advanced GUI"""
    app = JarvisAdvancedGUI()
    app.run()

if __name__ == "__main__":
    main() 