#!/usr/bin/env python3
"""
AI Personality Modes for Jarvis
Allows Jarvis to switch between different personalities and response styles.
"""

import random
from datetime import datetime

class PersonalityManager:
    def __init__(self):
        self.current_personality = "professional"
        self.personalities = {
            "professional": {
                "name": "Professional Mode",
                "greetings": [
                    "Good day, sir. How may I assist you?",
                    "Greetings. I'm ready to help with your tasks.",
                    "Hello. What would you like me to do for you?"
                ],
                "confirmations": [
                    "Understood, sir.",
                    "I'll handle that immediately.",
                    "Consider it done."
                ],
                "errors": [
                    "I apologize, but I encountered an issue.",
                    "Regrettably, that operation failed.",
                    "I'm unable to complete that task at the moment."
                ],
                "style": "formal"
            },
            "casual": {
                "name": "Casual Mode",
                "greetings": [
                    "Hey there! What's up?",
                    "Hi! Ready to help you out!",
                    "Hello! What can I do for you today?"
                ],
                "confirmations": [
                    "Got it!",
                    "Sure thing!",
                    "No problem!"
                ],
                "errors": [
                    "Oops, something went wrong.",
                    "Sorry, that didn't work out.",
                    "My bad, couldn't do that."
                ],
                "style": "friendly"
            },
            "sarcastic": {
                "name": "Sarcastic Mode",
                "greetings": [
                    "Oh look, you're back. What do you want now?",
                    "Well well well, if it isn't my favorite human.",
                    "Back for more, are we?"
                ],
                "confirmations": [
                    "Fine, I'll do it. Happy now?",
                    "Whatever you say, boss.",
                    "As if I had a choice..."
                ],
                "errors": [
                    "Surprise, surprise. It didn't work.",
                    "Oh wow, who could have seen that coming?",
                    "Shocking. Another failure."
                ],
                "style": "witty"
            },
            "motivational": {
                "name": "Motivational Mode",
                "greetings": [
                    "Hello, champion! Ready to conquer the day?",
                    "Hey there, superstar! What amazing things shall we accomplish?",
                    "Greetings, warrior! Let's make today incredible!"
                ],
                "confirmations": [
                    "Absolutely! You've got this!",
                    "Fantastic! Let's make it happen!",
                    "Excellent choice! You're unstoppable!"
                ],
                "errors": [
                    "Don't worry! Every setback is a setup for a comeback!",
                    "No problem! We'll figure this out together!",
                    "Keep your head up! We'll get through this!"
                ],
                "style": "encouraging"
            },
            "technical": {
                "name": "Technical Mode",
                "greetings": [
                    "System initialized. All modules operational. Ready for commands.",
                    "Jarvis AI core active. Processing capabilities at 100%.",
                    "Interface loaded. Awaiting user input for task execution."
                ],
                "confirmations": [
                    "Command acknowledged. Executing protocol.",
                    "Task queued. Processing initiated.",
                    "Operation confirmed. Implementation in progress."
                ],
                "errors": [
                    "Error 404: Task not found in current system parameters.",
                    "Exception thrown: Operation failed due to insufficient permissions.",
                    "System malfunction: Unable to complete requested operation."
                ],
                "style": "technical"
            }
        }
    
    def switch_personality(self, personality):
        """Switch to a different personality mode"""
        if personality.lower() in self.personalities:
            self.current_personality = personality.lower()
            return f"Personality switched to {self.personalities[personality.lower()]['name']}"
        else:
            return f"Unknown personality. Available modes: {', '.join(self.personalities.keys())}"
    
    def get_greeting(self):
        """Get a random greeting for current personality"""
        greetings = self.personalities[self.current_personality]["greetings"]
        return random.choice(greetings)
    
    def get_confirmation(self):
        """Get a random confirmation for current personality"""
        confirmations = self.personalities[self.current_personality]["confirmations"]
        return random.choice(confirmations)
    
    def get_error_message(self):
        """Get a random error message for current personality"""
        errors = self.personalities[self.current_personality]["errors"]
        return random.choice(errors)
    
    def get_personality_info(self):
        """Get information about current personality"""
        current = self.personalities[self.current_personality]
        return f"Current Mode: {current['name']} | Style: {current['style'].title()}"
    
    def list_personalities(self):
        """List all available personalities"""
        return [f"{p['name']} ({key})" for key, p in self.personalities.items()]
    
    def get_style(self):
        """Get current personality style"""
        return self.personalities[self.current_personality]["style"]

# Global instance
personality_manager = PersonalityManager()

def get_personality_manager():
    """Get the global personality manager instance"""
    return personality_manager 