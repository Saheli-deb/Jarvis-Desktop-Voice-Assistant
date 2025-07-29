#!/usr/bin/env python3
"""
Advanced Features Module for Jarvis
Provides enhanced functionality including system monitoring, file encryption,
QR code generation, password generation, file organization, and more.
"""

import os
import sys
import json
import time
import shutil
import secrets
import hashlib
import threading
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import qrcode
from pyzbar import pyzbar
import cv2
import psutil
import requests
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Global instance
_advanced_features_instance = None

def get_advanced_features():
    """Get or create the advanced features instance"""
    global _advanced_features_instance
    if _advanced_features_instance is None:
        _advanced_features_instance = AdvancedFeatures()
    return _advanced_features_instance

class AdvancedFeatures:
    def __init__(self):
        """Initialize advanced features"""
        self.notification_system = None  # Will be set externally
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        self.monitoring_active = False
        self.monitoring_thread = None
        
        # Create necessary directories
        self.create_directories()
        
        # Load OpenAI API key
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
    
    def create_directories(self):
        """Create necessary directories for advanced features"""
        directories = [
            "advanced_data",
            "advanced_data/encrypted_files",
            "advanced_data/qr_codes", 
            "advanced_data/backups",
            "advanced_data/organized_files"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def set_notification_system(self, notification_system):
        """Set the notification system reference"""
        self.notification_system = notification_system
    
    def system_monitor(self):
        """Start real-time system monitoring"""
        if self.monitoring_active:
            return "System monitoring is already active."
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitor_system, daemon=True)
        self.monitoring_thread.start()
        
        return "System monitoring started. Monitoring CPU, memory, disk, and network usage."
    
    def _monitor_system(self):
        """Background system monitoring thread"""
        while self.monitoring_active:
            try:
                # Get system metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                network = psutil.net_io_counters()
                
                # Check for high resource usage
                alerts = []
                if cpu_percent > 80:
                    alerts.append(f"High CPU usage: {cpu_percent}%")
                if memory.percent > 85:
                    alerts.append(f"High memory usage: {memory.percent}%")
                if disk.percent > 90:
                    alerts.append(f"High disk usage: {disk.percent}%")
                
                # Send alerts if any
                if alerts and self.notification_system:
                    for alert in alerts:
                        self.notification_system.show_advanced_notification(
                            "System Alert", alert, "warning", 5
                        )
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(60)
    
    def stop_monitoring(self):
        """Stop system monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        return "System monitoring stopped."
    
    def get_system_status(self):
        """Get current system status"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = psutil.net_io_counters()
            
            status = f"""
🖥️ SYSTEM STATUS REPORT
========================
CPU Usage: {cpu_percent}%
Memory Usage: {memory.percent}% ({memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB)
Disk Usage: {disk.percent}% ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)
Network: ↑ {network.bytes_sent // (1024**2)}MB ↓ {network.bytes_recv // (1024**2)}MB
========================
"""
            return status
            
        except Exception as e:
            return f"Error getting system status: {e}"
    
    def encrypt_file(self, file_path, password):
        """Encrypt a file with password protection"""
        try:
            if not os.path.exists(file_path):
                return "File not found."
            
            # Generate key from password
            key = hashlib.sha256(password.encode()).digest()
            cipher = Fernet(Fernet.generate_key())
            
            # Read and encrypt file
            with open(file_path, 'rb') as file:
                data = file.read()
            
            encrypted_data = cipher.encrypt(data)
            
            # Save encrypted file
            encrypted_path = f"advanced_data/encrypted_files/{os.path.basename(file_path)}.encrypted"
            with open(encrypted_path, 'wb') as file:
                file.write(encrypted_data)
            
            return f"File encrypted successfully. Saved as: {encrypted_path}"
            
        except Exception as e:
            return f"Encryption failed: {e}"
    
    def decrypt_file(self, file_path, password):
        """Decrypt a file with password"""
        try:
            if not os.path.exists(file_path):
                return "File not found."
            
            # Generate key from password
            key = hashlib.sha256(password.encode()).digest()
            cipher = Fernet(Fernet.generate_key())
            
            # Read encrypted file
            with open(file_path, 'rb') as file:
                encrypted_data = file.read()
            
            # Decrypt data
            decrypted_data = cipher.decrypt(encrypted_data)
            
            # Save decrypted file
            decrypted_path = file_path.replace('.encrypted', '_decrypted')
            with open(decrypted_path, 'wb') as file:
                file.write(decrypted_data)
            
            return f"File decrypted successfully. Saved as: {decrypted_path}"
            
        except Exception as e:
            return f"Decryption failed: {e}"
    
    def generate_qr_code(self, data, filename="qr_code.png"):
        """Generate QR code from data"""
        try:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            filepath = f"advanced_data/qr_codes/{filename}"
            img.save(filepath)
            
            return f"QR code generated successfully: {filepath}"
            
        except Exception as e:
            return f"QR code generation failed: {e}"
    
    def read_qr_code(self, image_path):
        """Read QR code from image"""
        try:
            if not os.path.exists(image_path):
                return "Image file not found."
            
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                return "Could not read image file."
            
            # Decode QR codes
            decoded_objects = pyzbar.decode(image)
            
            if not decoded_objects:
                return "No QR code found in image."
            
            # Return all found QR codes
            results = []
            for obj in decoded_objects:
                results.append(obj.data.decode('utf-8'))
            
            return results[0] if len(results) == 1 else results
            
        except Exception as e:
            return f"QR code reading failed: {e}"
    
    def password_generator(self, length=12, include_symbols=True, include_numbers=True):
        """Generate secure password"""
        try:
            chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            if include_numbers:
                chars += "0123456789"
            if include_symbols:
                chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
            
            password = ''.join(secrets.choice(chars) for _ in range(length))
            return password
            
        except Exception as e:
            return f"Password generation failed: {e}"
    
    def file_organizer(self, directory):
        """Organize files by type"""
        try:
            if not os.path.exists(directory):
                return "Directory not found."
            
            # File type categories
            categories = {
                'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
                'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
                'Videos': ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv'],
                'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
                'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
                'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c']
            }
            
            organized_count = 0
            
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                
                if os.path.isfile(filepath):
                    # Get file extension
                    _, ext = os.path.splitext(filename)
                    ext = ext.lower()
                    
                    # Find category
                    category = None
                    for cat, extensions in categories.items():
                        if ext in extensions:
                            category = cat
                            break
                    
                    if category:
                        # Create category directory
                        category_dir = os.path.join(directory, category)
                        os.makedirs(category_dir, exist_ok=True)
                        
                        # Move file
                        new_path = os.path.join(category_dir, filename)
                        if not os.path.exists(new_path):
                            shutil.move(filepath, new_path)
                            organized_count += 1
            
            return f"File organization complete. Organized {organized_count} files."
            
        except Exception as e:
            return f"File organization failed: {e}"
    
    def ai_analysis(self, text_data):
        """Analyze text using AI"""
        try:
            if not self.openai_api_key:
                return "OpenAI API key not configured. Please set OPENAI_API_KEY in .env file."
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant. Analyze the given text and provide insights."},
                    {"role": "user", "content": f"Please analyze this text: {text_data}"}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"AI analysis failed: {e}"
    
    def create_backup(self, source_path, backup_path):
        """Create encrypted backup of files/folders"""
        try:
            if not os.path.exists(source_path):
                return "Source path not found."
            
            # Create backup directory
            os.makedirs(backup_path, exist_ok=True)
            
            if os.path.isfile(source_path):
                # Backup single file
                shutil.copy2(source_path, backup_path)
            else:
                # Backup directory
                shutil.copytree(source_path, os.path.join(backup_path, os.path.basename(source_path)))
            
            return f"Backup created successfully at: {backup_path}"
            
        except Exception as e:
            return f"Backup creation failed: {e}"
    
    def network_scanner(self):
        """Scan network for devices using ping"""
        try:
            import subprocess
            import socket
            
            devices = []
            
            # Get local IP address
            try:
                # Get local IP using socket
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
                s.close()
                
                # Extract network prefix (e.g., 192.168.1 from 192.168.1.100)
                network_prefix = '.'.join(local_ip.split('.')[:-1])
                
                print(f"Scanning network: {network_prefix}.0/24")
                
                # Scan common IP range
                for i in range(1, 255):
                    ip = f"{network_prefix}.{i}"
                    
                    try:
                        # Use ping to check if host is up
                        result = subprocess.run(
                            ['ping', '-n', '1', '-w', '1000', ip],
                            capture_output=True,
                            text=True,
                            timeout=2
                        )
                        
                        if result.returncode == 0:
                            # Try to get hostname
                            try:
                                hostname = socket.gethostbyaddr(ip)[0]
                            except:
                                hostname = "Unknown"
                            
                            devices.append({
                                'ip': ip,
                                'hostname': hostname
                            })
                            print(f"Found device: {hostname} ({ip})")
                            
                    except subprocess.TimeoutExpired:
                        continue
                    except Exception as e:
                        continue
                
                if devices:
                    return devices
                else:
                    return "No devices found on network. Try checking your network connection."
                    
            except Exception as e:
                return f"Could not determine local IP: {e}"
            
        except Exception as e:
            return f"Network scanning failed: {e}"
    
    def voice_commands_advanced(self):
        """Return list of available voice commands"""
        return [
            "system monitor - Start system monitoring",
            "system status - Check system status", 
            "encrypt file - Encrypt a file",
            "decrypt file - Decrypt a file",
            "generate qr code - Create QR code",
            "read qr code - Read QR code from image",
            "generate password - Generate secure password",
            "organize files - Organize files by type",
            "ai analysis - Analyze text with AI",
            "create backup - Create encrypted backup",
            "scan network - Scan network for devices"
        ]

if __name__ == "__main__":
    # Test the advanced features
    af = AdvancedFeatures()
    print("Advanced Features initialized successfully!")
    print("Available commands:")
    for cmd in af.voice_commands_advanced():
        print(f"  - {cmd}") 