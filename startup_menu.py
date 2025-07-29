#!/usr/bin/env python3
"""
Startup Menu for Jarvis
Displays all available features and commands when Jarvis starts.
"""

import os
import time
from datetime import datetime

def display_startup_menu():
    """Display comprehensive startup menu with all Jarvis features"""
    
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # ASCII Art Banner
    banner = """
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                              ║
    ║    ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗    ███████╗██╗  ██╗███████╗  ║
    ║    ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝    ██╔════╝██║  ██║██╔════╝  ║
    ║    ██║███████║██████╔╝██║   ██║██║███████╗    ███████╗███████║███████╗  ║
    ║    ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║    ╚════██║██╔══██║╚════██║  ║
    ║    ██║██║  ██║██║  ██║ ╚████╔╝ ██║███████║    ███████║██║  ██║███████║  ║
    ║    ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝    ╚══════╝╚═╝  ╚═╝╚══════╝  ║
    ║                                                                              ║
    ║                    🤖 ADVANCED AI ASSISTANT v2.0 🤖                        ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """
    
    print(banner)
    
    # Current time and date
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"🕐 Started at: {current_time}")
    print("=" * 80)
    
    # Feature Categories
    categories = [
        {
            "name": "🎭 AI PERSONALITY MODES",
            "description": "Switch between 5 different AI personalities",
            "commands": [
                "Jarvis, switch personality",
                "Jarvis, personality info", 
                "Jarvis, list personalities",
                "Jarvis, switch ai context",
                "Jarvis, change ai mode"
            ]
        },
        {
            "name": "🤖 ENHANCED AI FEATURES",
            "description": "GPT-4, DALL-E 3, Whisper integration",
            "commands": [
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
            ]
        },
        {
            "name": "📊 ANALYTICS DASHBOARD",
            "description": "Track usage and system performance",
            "commands": [
                "Jarvis, show my stats",
                "Jarvis, usage statistics",
                "Jarvis, system performance report"
            ]
        },
        {
            "name": "🎮 VOICE GAMES",
            "description": "Interactive games using only voice",
            "commands": [
                "Jarvis, start trivia",
                "Jarvis, start word game", 
                "Jarvis, start story",
                "Jarvis, game status"
            ]
        },
        {
            "name": "🔧 ADVANCED FEATURES",
            "description": "File encryption, QR codes, network scanning",
            "commands": [
                "Jarvis, system monitor",
                "Jarvis, encrypt file",
                "Jarvis, generate qr code",
                "Jarvis, generate password",
                "Jarvis, organize files",
                "Jarvis, scan network"
            ]
        },
        {
            "name": "📋 REMINDER & TODO",
            "description": "Smart task management",
            "commands": [
                "Jarvis, add reminder",
                "Jarvis, add todo",
                "Jarvis, list reminders",
                "Jarvis, list todos"
            ]
        },
        {
            "name": "📧 EMAIL & CALENDAR",
            "description": "Email and calendar management",
            "commands": [
                "Jarvis, send email to",
                "Jarvis, read my emails",
                "Jarvis, add calendar event",
                "Jarvis, list calendar events"
            ]
        },
        {
            "name": "🎵 MULTIMEDIA & ENTERTAINMENT",
            "description": "Photos, news, music, and more",
            "commands": [
                "Jarvis, click my photo",
                "Jarvis, news",
                "Jarvis, send whatsapp",
                "Jarvis, generate image",
                "Jarvis, tired",
                "Jarvis, screenshot"
            ]
        },
        {
            "name": "🎮 MEDIA CONTROL",
            "description": "Video and audio control",
            "commands": [
                "Jarvis, pause",
                "Jarvis, play",
                "Jarvis, mute",
                "Jarvis, youtube automation",
                "Jarvis, volume up",
                "Jarvis, volume down"
            ]
        },
        {
            "name": "🖥️ SYSTEM CONTROL",
            "description": "System and application control",
            "commands": [
                "Jarvis, shutdown",
                "Jarvis, restart",
                "Jarvis, open",
                "Jarvis, close",
                "Jarvis, scroll up",
                "Jarvis, scroll down"
            ]
        },
        {
            "name": "🌐 WEB & SEARCH",
            "description": "Web search and browsing",
            "commands": [
                "Jarvis, google",
                "Jarvis, youtube",
                "Jarvis, wikipedia"
            ]
        },
        {
            "name": "🌤️ WEATHER & TIME",
            "description": "Weather and time information",
            "commands": [
                "Jarvis, temperature",
                "Jarvis, weather",
                "Jarvis, the time"
            ]
        },
        {
            "name": "🔋 SYSTEM INFO",
            "description": "System information and utilities",
            "commands": [
                "Jarvis, battery",
                "Jarvis, set an alarm",
                "Jarvis, calculate"
            ]
        },
        {
            "name": "💬 CHAT & REMEMBRANCE",
            "description": "Chatbot and memory features",
            "commands": [
                "Jarvis, jarvis bot",
                "Jarvis, remember that",
                "Jarvis, what do you remember"
            ]
        }
    ]
    
    # Display categories
    print("\n📋 AVAILABLE FEATURE CATEGORIES:")
    print("=" * 80)
    
    for i, category in enumerate(categories, 1):
        print(f"\n{i:2d}. {category['name']}")
        print(f"    📝 {category['description']}")
        print(f"    🎯 Sample Commands:")
        for cmd in category['commands'][:3]:  # Show first 3 commands
            print(f"       • {cmd}")
        if len(category['commands']) > 3:
            print(f"       • ... and {len(category['commands']) - 3} more")
    
    # Quick Start Guide
    print("\n" + "=" * 80)
    print("🚀 QUICK START GUIDE:")
    print("=" * 80)
    print("1. Say 'Jarvis, wake up' to start")
    print("2. Try 'Jarvis, ai chat' for advanced AI conversation")
    print("3. Say 'Jarvis, switch personality' to change AI mode")
    print("4. Try 'Jarvis, start trivia' for voice games")
    print("5. Say 'Jarvis, show my stats' to view analytics")
    print("6. Try 'Jarvis, generate ai image' for AI image creation")
    print("7. Say 'Jarvis, code help' for programming assistance")
    print("8. Say 'Jarvis, go to sleep' when done")
    
    # Statistics
    total_commands = sum(len(cat['commands']) for cat in categories)
    total_categories = len(categories)
    
    print("\n" + "=" * 80)
    print("📊 JARVIS STATISTICS:")
    print("=" * 80)
    print(f"🎯 Total Voice Commands: {total_commands}+")
    print(f"📂 Feature Categories: {total_categories}")
    print(f"🤖 AI Personalities: 5")
    print(f"🎮 Voice Games: 3 types")
    print(f"🔧 Advanced Features: 12+")
    print(f"📊 Analytics: Real-time tracking")
    
    # Unique Features
    print("\n" + "=" * 80)
    print("⭐ UNIQUE FEATURES:")
    print("=" * 80)
    unique_features = [
        "🎭 AI Personality Modes - 5 different AI personalities",
        "🤖 Enhanced AI Features - GPT-4, DALL-E 3, Whisper integration", 
        "🎮 Voice Games - Interactive games using only voice",
        "📊 Analytics Dashboard - Track usage and performance",
        "🔧 Advanced Features - File encryption, QR codes, network scanning",
        "📱 Smart Notifications - Real-time desktop notifications",
        "🎨 Image Generation - Create images with AI",
        "💻 Code Assistance - Programming help with AI",
        "🌐 Multi-language Support - Translation capabilities",
        "📈 Research Assistant - AI-powered research"
    ]
    
    for feature in unique_features:
        print(f"   {feature}")
    
    print("\n" + "=" * 80)
    print("🎉 Your Jarvis is now ready! Say 'Jarvis, wake up' to begin.")
    print("=" * 80)
    
    # Wait a moment for user to read
    time.sleep(3)

def get_feature_count():
    """Get total number of features"""
    categories = [
        "AI Personality Modes", "Enhanced AI Features", "Analytics Dashboard",
        "Voice Games", "Advanced Features", "Reminder & Todo", "Email & Calendar",
        "Multimedia & Entertainment", "Media Control", "System Control",
        "Web & Search", "Weather & Time", "System Info", "Chat & Remembrance"
    ]
    return len(categories)

def get_command_count():
    """Get total number of commands"""
    return 114  # Based on our complete features list

if __name__ == "__main__":
    display_startup_menu() 