#!/usr/bin/env python3
"""
Jarvis Launcher
Combines GUI and console interfaces for Jarvis
"""

import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os
import threading
import time

class JarvisLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("JARVIS Launcher")
        self.root.geometry("600x400")
        self.root.configure(bg='#0a0a0a')
        
        # Colors
        self.colors = {
            'bg_dark': '#0a0a0a',
            'bg_medium': '#1a1a1a',
            'red_primary': '#ff0000',
            'text_white': '#ffffff',
            'text_gray': '#cccccc'
        }
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create launcher interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame,
                             text="JARVIS LAUNCHER",
                             font=('Arial Black', 24, 'bold'),
                             fg=self.colors['red_primary'],
                             bg=self.colors['bg_dark'])
        title_label.pack(pady=(0, 20))
        
        # Subtitle
        subtitle_label = tk.Label(main_frame,
                                text="Choose your preferred interface",
                                font=('Arial', 12),
                                fg=self.colors['text_gray'],
                                bg=self.colors['bg_dark'])
        subtitle_label.pack(pady=(0, 30))
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        buttons_frame.pack(expand=True)
        
        # GUI Button
        gui_btn = tk.Button(buttons_frame,
                           text="🚀 LAUNCH GUI VERSION",
                           font=('Arial Black', 14, 'bold'),
                           fg=self.colors['text_white'],
                           bg=self.colors['red_primary'],
                           activebackground=self.colors['red_primary'],
                           activeforeground=self.colors['text_white'],
                           relief='flat',
                           bd=0,
                           padx=30,
                           pady=15,
                           command=self.launch_gui)
        gui_btn.pack(pady=10)
        
        # Console Button
        console_btn = tk.Button(buttons_frame,
                              text="💻 LAUNCH CONSOLE VERSION",
                              font=('Arial Black', 14, 'bold'),
                              fg=self.colors['text_white'],
                              bg=self.colors['bg_medium'],
                              activebackground=self.colors['red_primary'],
                              activeforeground=self.colors['text_white'],
                              relief='flat',
                              bd=0,
                              padx=30,
                              pady=15,
                              command=self.launch_console)
        console_btn.pack(pady=10)
        
        # Advanced GUI Button
        advanced_btn = tk.Button(buttons_frame,
                               text="✨ LAUNCH ADVANCED GUI",
                               font=('Arial Black', 14, 'bold'),
                               fg=self.colors['text_white'],
                               bg=self.colors['red_primary'],
                               activebackground=self.colors['red_primary'],
                               activeforeground=self.colors['text_white'],
                               relief='flat',
                               bd=0,
                               padx=30,
                               pady=15,
                               command=self.launch_advanced_gui)
        advanced_btn.pack(pady=10)
        
        # Info frame
        info_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        info_frame.pack(pady=20)
        
        info_text = """
        🎯 JARVIS v2.0 - Advanced AI Assistant
        
        Features:
        • 114+ Voice Commands
        • 14 Feature Categories
        • 5 AI Personalities
        • 3 Voice Games
        • 12+ Advanced Features
        
        Choose your preferred interface to start Jarvis!
        """
        
        info_label = tk.Label(info_frame,
                            text=info_text,
                            font=('Arial', 10),
                            fg=self.colors['text_gray'],
                            bg=self.colors['bg_dark'],
                            justify='left')
        info_label.pack()
        
    def launch_gui(self):
        """Launch the basic GUI version"""
        try:
            self.root.withdraw()  # Hide launcher
            subprocess.Popen([sys.executable, 'jarvis_gui.py'])
            self.root.after(2000, self.root.destroy)  # Close launcher after 2 seconds
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch GUI: {str(e)}")
            self.root.deiconify()  # Show launcher again
            
    def launch_console(self):
        """Launch the console version"""
        try:
            self.root.withdraw()  # Hide launcher
            subprocess.Popen([sys.executable, 'jarvis_main.py'])
            self.root.after(2000, self.root.destroy)  # Close launcher after 2 seconds
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch console: {str(e)}")
            self.root.deiconify()  # Show launcher again
            
    def launch_advanced_gui(self):
        """Launch the advanced GUI version"""
        try:
            self.root.withdraw()  # Hide launcher
            subprocess.Popen([sys.executable, 'jarvis_gui_advanced.py'])
            self.root.after(2000, self.root.destroy)  # Close launcher after 2 seconds
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch advanced GUI: {str(e)}")
            self.root.deiconify()  # Show launcher again
            
    def run(self):
        """Start the launcher"""
        self.root.mainloop()

def main():
    """Main function"""
    launcher = JarvisLauncher()
    launcher.run()

if __name__ == "__main__":
    main() 