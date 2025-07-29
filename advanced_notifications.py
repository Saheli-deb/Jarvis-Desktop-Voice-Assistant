import os
import json
import threading
import time
from datetime import datetime, timedelta
from plyer import notification
import winsound
import tkinter as tk
from tkinter import messagebox
import webbrowser
import subprocess
import platform

class AdvancedNotificationSystem:
    def __init__(self):
        self.notification_thread = None
        self.stop_notifications = False
        self.notification_sound = True
        self.notification_style = "default"  # default, modern, minimal
        self.auto_open_links = False
        self.notification_history = []
        self.max_history = 100
        
    def show_advanced_notification(self, title, message, notification_type="info", 
                                 duration=10, sound=True, action_url=None, 
                                 priority="normal", icon_path=None):
        """
        Show an advanced desktop notification with multiple features
        """
        try:
            # Add to history
            self.add_to_history(title, message, notification_type, priority)
            
            # Play sound based on notification type
            if sound and self.notification_sound:
                self.play_notification_sound(notification_type)
            
            # Show desktop notification
            notification.notify(
                title=f"{self.get_emoji(notification_type)} {title}",
                message=message,
                app_icon=icon_path,
                timeout=duration,
            )
            
            # Auto-open links if enabled
            if action_url and self.auto_open_links:
                threading.Timer(2.0, lambda: webbrowser.open(action_url)).start()
            
            # Log notification
            print(f"🔔 {notification_type.upper()}: {title} - {message}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to show notification: {e}")
            return False
    
    def get_emoji(self, notification_type):
        """Get appropriate emoji for notification type"""
        emojis = {
            "reminder": "⏰",
            "todo": "📋",
            "alarm": "🔔",
            "warning": "⚠️",
            "error": "❌",
            "success": "✅",
            "info": "ℹ️",
            "urgent": "🚨",
            "calendar": "📅",
            "email": "📧",
            "message": "💬",
            "system": "⚙️"
        }
        return emojis.get(notification_type, "ℹ️")
    
    def play_notification_sound(self, notification_type):
        """Play different sounds based on notification type"""
        try:
            if platform.system() == "Windows":
                # Windows system sounds
                sounds = {
                    "reminder": winsound.SND_ALIAS_SYSTEMASTERISK,
                    "alarm": winsound.SND_ALIAS_SYSTEMHAND,
                    "urgent": winsound.SND_ALIAS_SYSTEMEXCLAMATION,
                    "success": winsound.SND_ALIAS_SYSTEMDEFAULT,
                    "error": winsound.SND_ALIAS_SYSTEMHAND,
                    "default": winsound.SND_ALIAS_SYSTEMASTERISK
                }
                
                sound = sounds.get(notification_type, sounds["default"])
                winsound.PlaySound(sound, winsound.SND_ALIAS)
            else:
                # For other platforms, use beep
                print("\a")  # Terminal bell
                
        except Exception as e:
            print(f"❌ Failed to play sound: {e}")
    
    def add_to_history(self, title, message, notification_type, priority):
        """Add notification to history"""
        notification_record = {
            "timestamp": datetime.now().isoformat(),
            "title": title,
            "message": message,
            "type": notification_type,
            "priority": priority
        }
        
        self.notification_history.append(notification_record)
        
        # Keep only recent notifications
        if len(self.notification_history) > self.max_history:
            self.notification_history.pop(0)
    
    def get_notification_history(self, limit=20):
        """Get recent notification history"""
        return self.notification_history[-limit:] if self.notification_history else []
    
    def clear_notification_history(self):
        """Clear notification history"""
        self.notification_history.clear()
    
    def show_popup_dialog(self, title, message, dialog_type="info"):
        """Show a popup dialog box"""
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            
            if dialog_type == "error":
                messagebox.showerror(title, message)
            elif dialog_type == "warning":
                messagebox.showwarning(title, message)
            elif dialog_type == "question":
                result = messagebox.askyesno(title, message)
                root.destroy()
                return result
            else:
                messagebox.showinfo(title, message)
            
            root.destroy()
            return True
            
        except Exception as e:
            print(f"❌ Failed to show popup dialog: {e}")
            return False
    
    def show_reminder_notification(self, reminder_data):
        """Show a specialized reminder notification"""
        title = f"Reminder: {reminder_data['title']}"
        message = f"Priority: {reminder_data['priority'].title()}\n"
        
        if reminder_data.get('description'):
            message += f"Description: {reminder_data['description']}\n"
        
        if reminder_data.get('due_date'):
            due_date = datetime.fromisoformat(reminder_data['due_date'])
            message += f"Due: {due_date.strftime('%B %d, %Y at %I:%M %p')}"
        
        return self.show_advanced_notification(
            title=title,
            message=message,
            notification_type="reminder",
            duration=15,
            sound=True,
            priority=reminder_data['priority']
        )
    
    def show_todo_notification(self, todo_data):
        """Show a specialized todo notification"""
        title = f"Todo: {todo_data['title']}"
        message = f"Priority: {todo_data['priority'].title()}\n"
        
        if todo_data.get('description'):
            message += f"Description: {todo_data['description']}"
        
        return self.show_advanced_notification(
            title=title,
            message=message,
            notification_type="todo",
            duration=12,
            sound=True,
            priority=todo_data['priority']
        )
    
    def show_system_notification(self, title, message, system_type="info"):
        """Show system-related notifications"""
        return self.show_advanced_notification(
            title=title,
            message=message,
            notification_type=system_type,
            duration=8,
            sound=True
        )
    
    def test_notification_system(self):
        """Test all notification types"""
        test_notifications = [
            ("Test Reminder", "This is a test reminder notification", "reminder"),
            ("Test Todo", "This is a test todo notification", "todo"),
            ("Test Alarm", "This is a test alarm notification", "alarm"),
            ("Test Warning", "This is a test warning notification", "warning"),
            ("Test Success", "This is a test success notification", "success"),
            ("Test Error", "This is a test error notification", "error"),
        ]
        
        for title, message, notif_type in test_notifications:
            self.show_advanced_notification(title, message, notif_type, duration=3)
            time.sleep(1)  # Small delay between notifications
    
    def configure_notifications(self, sound=True, style="default", auto_open_links=False):
        """Configure notification settings"""
        self.notification_sound = sound
        self.notification_style = style
        self.auto_open_links = auto_open_links
        print(f"🔧 Notification settings updated: Sound={sound}, Style={style}, Auto-open={auto_open_links}")

# Global notification system instance
notification_system = AdvancedNotificationSystem()

def get_notification_system():
    """Get the global notification system instance"""
    return notification_system 