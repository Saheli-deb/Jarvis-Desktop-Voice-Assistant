#!/usr/bin/env python3
"""
JARVIS Web UI Launcher
======================

This script launches the web-based user interface for JARVIS.
It automatically checks dependencies and starts the Flask server.

Usage:
    python start_ui.py
    
Then open your browser and go to: http://localhost:5000
"""

import sys
import subprocess
import os
import webbrowser
import time
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n🔧 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies!")
        print("Please run manually: pip install -r requirements.txt")
        return False
    except FileNotFoundError:
        print("❌ requirements.txt not found!")
        return False

def check_flask():
    """Check if Flask is available"""
    try:
        import flask
        print(f"✅ Flask version: {flask.__version__}")
        return True
    except ImportError:
        print("❌ Flask not found!")
        return False

def start_server():
    """Start the Flask server"""
    print("\n🚀 Starting JARVIS Web UI...")
    print("🌐 Server will be available at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    
    # Wait a moment then open browser
    def open_browser():
        time.sleep(3)
        try:
            webbrowser.open("http://localhost:5000")
            print("🌐 Opening browser...")
        except Exception as e:
            print(f"⚠️  Could not open browser automatically: {e}")
            print("Please manually open: http://localhost:5000")
    
    import threading
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start Flask app
    try:
        from app import app
        app.run(debug=False, host='0.0.0.0', port=5000)
    except ImportError:
        print("❌ Could not import Flask app!")
        print("Make sure app.py is in the current directory.")
        return False
    except KeyboardInterrupt:
        print("\n👋 Shutting down JARVIS Web UI...")
        return True
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

def main():
    """Main launcher function"""
    print("=" * 50)
    print("🤖 JARVIS Web UI Launcher")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check if we're in the right directory
    if not Path("app.py").exists():
        print("❌ app.py not found in current directory!")
        print("Please run this script from the JARVIS project directory.")
        return
    
    # Check Flask
    if not check_flask():
        print("\n📦 Installing Flask and dependencies...")
        if not install_dependencies():
            return
    
    # Start the server
    print("\n" + "=" * 50)
    start_server()

if __name__ == "__main__":
    main()