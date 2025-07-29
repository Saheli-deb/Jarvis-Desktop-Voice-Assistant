#!/usr/bin/env python3
"""
Advanced Features Installation Script for Jarvis AI Assistant
This script installs all required dependencies for the advanced features.
"""

import subprocess
import sys
import os
import platform

def print_banner():
    """Print installation banner"""
    print("=" * 60)
    print("🚀 JARVIS ADVANCED FEATURES INSTALLATION")
    print("=" * 60)
    print("Installing advanced features and dependencies...")
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_package(package):
    """Install a single package"""
    try:
        print(f"📦 Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}")
        return False

def install_requirements():
    """Install all requirements from requirements_advanced.txt"""
    try:
        print("📦 Installing advanced dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_advanced.txt"])
        print("✅ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install some dependencies")
        return False

def install_optional_dependencies():
    """Install optional dependencies"""
    optional_packages = [
        "python-nmap",
        "dlib",
        "opencv-python",
        "face-recognition"
    ]
    
    print("\n🔧 Installing optional dependencies...")
    for package in optional_packages:
        install_package(package)

def check_system_requirements():
    """Check system requirements"""
    print("\n🔍 Checking system requirements...")
    
    # Check OS
    os_name = platform.system()
    print(f"Operating System: {os_name}")
    
    if os_name == "Windows":
        print("✅ Windows detected - all features supported")
    elif os_name == "Linux":
        print("⚠️  Linux detected - some features may require additional setup")
    elif os_name == "Darwin":
        print("⚠️  macOS detected - some features may require additional setup")
    
    # Check for microphone
    try:
        import speech_recognition
        print("✅ Speech recognition available")
    except ImportError:
        print("❌ Speech recognition not available")
    
    # Check for camera (optional)
    try:
        import cv2
        print("✅ OpenCV available for camera features")
    except ImportError:
        print("⚠️  OpenCV not available - camera features disabled")

def create_directories():
    """Create necessary directories"""
    directories = [
        "backups",
        "face_data",
        "qr_codes",
        "encrypted_files",
        "system_logs"
    ]
    
    print("\n📁 Creating directories...")
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"📁 Directory exists: {directory}")

def test_installations():
    """Test if installations work correctly"""
    print("\n🧪 Testing installations...")
    
    tests = [
        ("Advanced Notifications", "from advanced_notifications import get_notification_system"),
        ("Advanced Features", "from advanced_features import get_advanced_features"),
        ("System Monitoring", "import psutil"),
        ("Image Processing", "import cv2"),
        ("QR Code", "import qrcode"),
        ("Encryption", "from cryptography.fernet import Fernet"),
        ("Face Recognition", "import face_recognition")
    ]
    
    for test_name, import_statement in tests:
        try:
            exec(import_statement)
            print(f"✅ {test_name} - OK")
        except ImportError as e:
            print(f"❌ {test_name} - Failed: {e}")
        except Exception as e:
            print(f"⚠️  {test_name} - Warning: {e}")

def show_next_steps():
    """Show next steps for user"""
    print("\n" + "=" * 60)
    print("🎉 INSTALLATION COMPLETE!")
    print("=" * 60)
    print("\n📋 Next Steps:")
    print("1. Run 'python jarvis_main.py' to start Jarvis")
    print("2. Say 'wake up' to activate Jarvis")
    print("3. Try these new voice commands:")
    print("   - 'test advanced notifications'")
    print("   - 'system monitor'")
    print("   - 'generate password'")
    print("   - 'ai analysis'")
    print("   - 'encrypt file'")
    print("   - 'generate qr code'")
    print("\n📚 Documentation:")
    print("- Read ADVANCED_FEATURES.md for detailed information")
    print("- Check requirements_advanced.txt for dependencies")
    print("\n🔧 Troubleshooting:")
    print("- If face recognition doesn't work, install dlib manually")
    print("- For network scanning, ensure nmap is installed")
    print("- Some features may require administrator privileges")
    print("\n🚀 Enjoy your enhanced Jarvis experience!")

def main():
    """Main installation function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check system requirements
    check_system_requirements()
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to install core dependencies")
        sys.exit(1)
    
    # Install optional dependencies
    install_optional_dependencies()
    
    # Create directories
    create_directories()
    
    # Test installations
    test_installations()
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Installation failed: {e}")
        sys.exit(1) 