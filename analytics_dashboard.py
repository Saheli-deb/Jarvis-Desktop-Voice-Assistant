#!/usr/bin/env python3
"""
Analytics Dashboard for Jarvis
Tracks user interactions, system performance, and provides detailed insights.
"""

import json
import os
import time
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import psutil

class AnalyticsDashboard:
    def __init__(self):
        self.data_file = "analytics_data.json"
        self.load_data()
        
    def load_data(self):
        """Load analytics data from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    self.data = json.load(f)
            else:
                self.data = {
                    "sessions": [],
                    "commands": [],
                    "system_performance": [],
                    "errors": [],
                    "personality_usage": {},
                    "daily_stats": {},
                    "voice_recognition": {
                        "successful": 0,
                        "failed": 0,
                        "total": 0
                    }
                }
        except Exception as e:
            print(f"Error loading analytics: {e}")
            self.data = {
                "sessions": [],
                "commands": [],
                "system_performance": [],
                "errors": [],
                "personality_usage": {},
                "daily_stats": {},
                "voice_recognition": {
                    "successful": 0,
                    "failed": 0,
                    "total": 0
                }
            }
    
    def save_data(self):
        """Save analytics data to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving analytics: {e}")
    
    def start_session(self):
        """Start a new user session"""
        session = {
            "start_time": datetime.now().isoformat(),
            "session_id": f"session_{int(time.time())}",
            "commands_used": 0,
            "errors_encountered": 0
        }
        self.data["sessions"].append(session)
        self.save_data()
        return session["session_id"]
    
    def end_session(self, session_id):
        """End a user session"""
        for session in self.data["sessions"]:
            if session["session_id"] == session_id:
                session["end_time"] = datetime.now().isoformat()
                session["duration"] = self.calculate_duration(session["start_time"], session["end_time"])
                break
        self.save_data()
    
    def log_command(self, command, success=True, response_time=None):
        """Log a voice command"""
        command_log = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "success": success,
            "response_time": response_time
        }
        self.data["commands"].append(command_log)
        
        # Update daily stats
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in self.data["daily_stats"]:
            self.data["daily_stats"][today] = {
                "commands": 0,
                "successful_commands": 0,
                "failed_commands": 0,
                "total_time": 0
            }
        
        self.data["daily_stats"][today]["commands"] += 1
        if success:
            self.data["daily_stats"][today]["successful_commands"] += 1
        else:
            self.data["daily_stats"][today]["failed_commands"] += 1
        
        self.save_data()
    
    def log_system_performance(self):
        """Log current system performance"""
        try:
            performance = {
                "timestamp": datetime.now().isoformat(),
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent,
                "network_io": dict(psutil.net_io_counters()._asdict())
            }
            self.data["system_performance"].append(performance)
            self.save_data()
        except Exception as e:
            print(f"Error logging system performance: {e}")
    
    def log_error(self, error_type, error_message, command=None):
        """Log an error"""
        error_log = {
            "timestamp": datetime.now().isoformat(),
            "error_type": error_type,
            "error_message": error_message,
            "command": command
        }
        self.data["errors"].append(error_log)
        self.save_data()
    
    def log_voice_recognition(self, success):
        """Log voice recognition success/failure"""
        self.data["voice_recognition"]["total"] += 1
        if success:
            self.data["voice_recognition"]["successful"] += 1
        else:
            self.data["voice_recognition"]["failed"] += 1
        self.save_data()
    
    def log_personality_usage(self, personality):
        """Log personality mode usage"""
        if personality not in self.data["personality_usage"]:
            self.data["personality_usage"][personality] = 0
        self.data["personality_usage"][personality] += 1
        self.save_data()
    
    def track_command(self, command, success=True):
        """Track a command for analytics (alias for log_command)"""
        return self.log_command(command, success)
    
    def get_usage_stats(self, days=7):
        """Get usage statistics for the last N days"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        stats = {
            "total_commands": 0,
            "successful_commands": 0,
            "failed_commands": 0,
            "total_sessions": 0,
            "avg_session_duration": 0,
            "most_used_commands": [],
            "personality_usage": {},
            "voice_recognition_rate": 0
        }
        
        # Filter data for the specified period
        recent_commands = [
            cmd for cmd in self.data["commands"]
            if datetime.fromisoformat(cmd["timestamp"]) >= start_date
        ]
        
        recent_sessions = [
            session for session in self.data["sessions"]
            if "end_time" in session and datetime.fromisoformat(session["start_time"]) >= start_date
        ]
        
        # Calculate statistics
        stats["total_commands"] = len(recent_commands)
        stats["successful_commands"] = len([cmd for cmd in recent_commands if cmd["success"]])
        stats["failed_commands"] = len([cmd for cmd in recent_commands if not cmd["success"]])
        stats["total_sessions"] = len(recent_sessions)
        
        # Calculate average session duration
        if recent_sessions:
            total_duration = sum(session.get("duration", 0) for session in recent_sessions)
            stats["avg_session_duration"] = total_duration / len(recent_sessions)
        
        # Most used commands
        command_counter = Counter(cmd["command"] for cmd in recent_commands)
        stats["most_used_commands"] = command_counter.most_common(10)
        
        # Personality usage
        stats["personality_usage"] = dict(self.data["personality_usage"])
        
        # Voice recognition rate
        total_voice = self.data["voice_recognition"]["total"]
        successful_voice = self.data["voice_recognition"]["successful"]
        if total_voice > 0:
            stats["voice_recognition_rate"] = (successful_voice / total_voice) * 100
        
        return stats
    
    def get_system_performance_report(self):
        """Get system performance report"""
        if not self.data["system_performance"]:
            return "No system performance data available."
        
        recent_performance = self.data["system_performance"][-100:]  # Last 100 entries
        
        avg_cpu = sum(p["cpu_percent"] for p in recent_performance) / len(recent_performance)
        avg_memory = sum(p["memory_percent"] for p in recent_performance) / len(recent_performance)
        avg_disk = sum(p["disk_percent"] for p in recent_performance) / len(recent_performance)
        
        return {
            "average_cpu_usage": f"{avg_cpu:.1f}%",
            "average_memory_usage": f"{avg_memory:.1f}%",
            "average_disk_usage": f"{avg_disk:.1f}%",
            "performance_entries": len(recent_performance)
        }
    
    def get_error_report(self, days=7):
        """Get error report for the last N days"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        recent_errors = [
            error for error in self.data["errors"]
            if datetime.fromisoformat(error["timestamp"]) >= start_date
        ]
        
        error_types = Counter(error["error_type"] for error in recent_errors)
        
        return {
            "total_errors": len(recent_errors),
            "error_types": dict(error_types),
            "recent_errors": recent_errors[-10:]  # Last 10 errors
        }
    
    def generate_detailed_report(self):
        """Generate a comprehensive analytics report"""
        stats = self.get_usage_stats(30)  # Last 30 days
        system_perf = self.get_system_performance_report()
        error_report = self.get_error_report(30)
        
        report = f"""
📊 JARVIS ANALYTICS REPORT
{'='*50}

📈 USAGE STATISTICS (Last 30 Days)
• Total Commands: {stats['total_commands']}
• Successful Commands: {stats['successful_commands']}
• Failed Commands: {stats['failed_commands']}
• Success Rate: {(stats['successful_commands']/stats['total_commands']*100):.1f}% if stats['total_commands'] > 0 else 0%
• Total Sessions: {stats['total_sessions']}
• Average Session Duration: {stats['avg_session_duration']:.1f} minutes

🎤 VOICE RECOGNITION
• Recognition Rate: {stats['voice_recognition_rate']:.1f}%
• Total Voice Attempts: {self.data['voice_recognition']['total']}
• Successful Recognitions: {self.data['voice_recognition']['successful']}

🔧 SYSTEM PERFORMANCE
• Average CPU Usage: {system_perf['average_cpu_usage']}
• Average Memory Usage: {system_perf['average_memory_usage']}
• Average Disk Usage: {system_perf['average_disk_usage']}

🚨 ERROR REPORT
• Total Errors: {error_report['total_errors']}
• Error Types: {error_report['error_types']}

🏆 TOP COMMANDS
"""
        
        for i, (command, count) in enumerate(stats['most_used_commands'][:5], 1):
            report += f"• {i}. '{command}': {count} times\n"
        
        report += f"""
🎭 PERSONALITY USAGE
"""
        for personality, count in stats['personality_usage'].items():
            report += f"• {personality.title()}: {count} times\n"
        
        return report
    
    def calculate_duration(self, start_time, end_time):
        """Calculate duration between two timestamps in minutes"""
        try:
            start = datetime.fromisoformat(start_time)
            end = datetime.fromisoformat(end_time)
            duration = (end - start).total_seconds() / 60
            return duration
        except:
            return 0

# Global instance
analytics_dashboard = AnalyticsDashboard()

def get_analytics_dashboard():
    """Get the global analytics dashboard instance"""
    return analytics_dashboard 