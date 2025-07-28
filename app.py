from flask import Flask, render_template, request, jsonify, session
import json
import threading
import time
from datetime import datetime
import speech_recognition as sr
import pyttsx3
import secrets

# Import existing Jarvis functions
try:
    from jarvis_main import takeCommand, chat_with_gpt, speak
    from NewsRead import latestnews
    from Calculatenumbers import Calc
    from SearchNow import searchGoogle
    from whatsapp_automation import send_whatsapp_message_auto
    from youtube_automation import control_youtube
    from handle_system import handle_system_command
    from GreetMe import greetMe
    from generate_img import generate_image
except ImportError as e:
    print(f"Warning: Some Jarvis modules not available: {e}")

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Global variables for conversation history
conversation_history = []
is_listening = False

class JarvisUI:
    def __init__(self):
        self.tts_engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
    def speak_text(self, text):
        """Convert text to speech"""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")
    
    def listen_for_speech(self):
        """Listen for voice input"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            text = self.recognizer.recognize_google(audio)
            return text.lower()
        except sr.WaitTimeoutError:
            return "timeout"
        except sr.UnknownValueError:
            return "could not understand"
        except Exception as e:
            return f"error: {str(e)}"

jarvis_ui = JarvisUI()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip().lower()
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Add user message to history
        conversation_history.append({
            'type': 'user',
            'message': user_message,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        })
        
        # Process the command
        response = process_jarvis_command(user_message)
        
        # Add Jarvis response to history
        conversation_history.append({
            'type': 'jarvis',
            'message': response,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        })
        
        return jsonify({
            'response': response,
            'history': conversation_history[-10:]  # Last 10 messages
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/voice-input', methods=['POST'])
def voice_input():
    global is_listening
    try:
        if is_listening:
            return jsonify({'error': 'Already listening'}), 400
        
        is_listening = True
        speech_text = jarvis_ui.listen_for_speech()
        is_listening = False
        
        if speech_text in ['timeout', 'could not understand'] or speech_text.startswith('error:'):
            return jsonify({'error': speech_text}), 400
        
        return jsonify({'speech_text': speech_text})
        
    except Exception as e:
        is_listening = False
        return jsonify({'error': str(e)}), 500

@app.route('/api/speak', methods=['POST'])
def speak_endpoint():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if text:
            # Run TTS in a separate thread to avoid blocking
            threading.Thread(target=jarvis_ui.speak_text, args=(text,)).start()
            return jsonify({'status': 'speaking'})
        
        return jsonify({'error': 'No text provided'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/quick-action', methods=['POST'])
def quick_action():
    try:
        data = request.get_json()
        action = data.get('action', '')
        
        response = process_quick_action(action)
        
        # Add to conversation history
        conversation_history.append({
            'type': 'user',
            'message': f"Quick action: {action}",
            'timestamp': datetime.now().strftime('%H:%M:%S')
        })
        
        conversation_history.append({
            'type': 'jarvis',
            'message': response,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        })
        
        return jsonify({
            'response': response,
            'history': conversation_history[-10:]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history')
def get_history():
    return jsonify({'history': conversation_history[-20:]})  # Last 20 messages

def process_jarvis_command(query):
    """Process user commands and return appropriate responses"""
    try:
        query = query.lower().strip()
        
        # Greeting commands
        if any(word in query for word in ["hello", "hi", "hey"]):
            return "Hello! I'm Jarvis, your AI assistant. How can I help you today?"
        
        elif "how are you" in query:
            return "I'm functioning perfectly, sir! Ready to assist you."
        
        elif "what can you do" in query or "help" in query:
            return """I can help you with:
            • Answer questions using AI
            • Read latest news
            • Send WhatsApp messages
            • Take screenshots
            • Control YouTube playback
            • Perform calculations
            • Search the web
            • Generate images
            • System commands (shutdown, restart)
            • And much more! Just ask me anything."""
        
        # News
        elif "news" in query:
            try:
                news_result = latestnews()
                return "I've started reading the latest news for you!"
            except:
                return "Sorry, I couldn't fetch the news right now."
        
        # Calculator
        elif "calculate" in query or "math" in query:
            calculation = query.replace("calculate", "").replace("math", "").strip()
            try:
                result = Calc(calculation)
                return f"The calculation result is: {result}"
            except:
                return "I couldn't perform that calculation. Please try a different format."
        
        # WhatsApp
        elif "whatsapp" in query or "send message" in query:
            try:
                send_whatsapp_message_auto()
                return "I'll help you send a WhatsApp message!"
            except:
                return "Sorry, I couldn't access WhatsApp right now."
        
        # YouTube controls
        elif "pause" in query:
            return "Video paused!"
        elif "play" in query and "youtube" not in query:
            return "Video resumed!"
        elif "mute" in query:
            return "Video muted!"
        
        # Search
        elif "search" in query or "google" in query:
            search_term = query.replace("search", "").replace("google", "").strip()
            try:
                searchGoogle(search_term)
                return f"I've searched Google for: {search_term}"
            except:
                return f"I'll search for: {search_term}"
        
        # Screenshot
        elif "screenshot" in query:
            return "Taking a screenshot now!"
        
        # Generate image
        elif "generate image" in query or "create image" in query:
            return "What image would you like me to generate? Please provide a description."
        
        # System commands
        elif any(cmd in query for cmd in ["shutdown", "restart", "log off"]):
            return "System command received. Please confirm this action."
        
        # ChatBot mode - anything else goes to GPT
        else:
            try:
                gpt_response = chat_with_gpt(query)
                return gpt_response
            except:
                return "I'm having trouble connecting to my AI brain right now. Please try again!"
                
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

def process_quick_action(action):
    """Process quick action buttons"""
    actions = {
        'news': 'Reading the latest news for you!',
        'weather': 'Let me check the weather for you!',
        'screenshot': 'Taking a screenshot now!',
        'whatsapp': 'Opening WhatsApp for you!',
        'youtube': 'What would you like me to do on YouTube?',
        'calculate': 'I\'m ready to perform calculations!',
        'greet': 'Hello! Great to see you today!'
    }
    
    return actions.get(action, f"Executing {action}...")

if __name__ == '__main__':
    print("🚀 Starting Jarvis Web UI...")
    print("🌐 Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)