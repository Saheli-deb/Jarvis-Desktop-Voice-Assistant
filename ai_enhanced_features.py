#!/usr/bin/env python3
"""
Enhanced AI Features for Jarvis
Advanced AI capabilities including GPT-4, image generation, voice cloning, and more.
"""

import openai
import os
import json
import requests
import base64
from datetime import datetime
import speech_recognition as sr
import pyttsx3
from PIL import Image
import io
import numpy as np
from dotenv import load_dotenv

load_dotenv()

class EnhancedAI:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.conversation_history = []
        self.voice_engine = pyttsx3.init("sapi5")
        self.voices = self.voice_engine.getProperty("voices")
        self.voice_engine.setProperty("voice", self.voices[0].id)
        self.voice_engine.setProperty("rate", 200)
        
        # AI Models configuration
        self.models = {
            "gpt-4": "gpt-4",
            "gpt-3.5": "gpt-3.5-turbo",
            "dall-e": "dall-e-3",
            "whisper": "whisper-1"
        }
        
        # Conversation contexts
        self.contexts = {
            "assistant": "You are Jarvis, an advanced AI assistant with multiple capabilities.",
            "creative": "You are a creative AI that helps with writing, brainstorming, and artistic projects.",
            "technical": "You are a technical expert specializing in programming, troubleshooting, and system analysis.",
            "educational": "You are an educational AI that explains complex topics in simple terms.",
            "business": "You are a business consultant helping with strategy, analysis, and decision-making."
        }
        self.current_context = "assistant"
        
    def set_context(self, context):
        """Set the AI conversation context"""
        if context in self.contexts:
            self.current_context = context
            return f"Context switched to {context} mode."
        return f"Unknown context. Available: {', '.join(self.contexts.keys())}"
    
    def advanced_chat(self, message, model="gpt-4", max_tokens=500):
        """Advanced chat with context and conversation history"""
        try:
            # Add system message with context
            messages = [
                {"role": "system", "content": self.contexts[self.current_context]},
                {"role": "system", "content": "You have access to conversation history and can provide detailed, helpful responses."}
            ]
            
            # Add conversation history (last 10 messages)
            for msg in self.conversation_history[-10:]:
                messages.append(msg)
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            reply = response['choices'][0]['message']['content']
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": reply})
            
            return reply
            
        except Exception as e:
            return f"AI chat error: {str(e)}"
    
    def generate_image(self, prompt, size="1024x1024", quality="standard"):
        """Generate images using DALL-E 3"""
        try:
            response = openai.Image.create(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality=quality,
                n=1
            )
            
            image_url = response['data'][0]['url']
            
            # Download and save the image
            img_response = requests.get(image_url)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_image_{timestamp}.png"
            
            with open(filename, "wb") as f:
                f.write(img_response.content)
            
            return f"Image generated and saved as {filename}"
            
        except Exception as e:
            return f"Image generation error: {str(e)}"
    
    def analyze_sentiment(self, text):
        """Analyze text sentiment using AI"""
        try:
            prompt = f"Analyze the sentiment of this text and provide a detailed analysis including emotion, tone, and confidence score (0-100): {text}"
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a sentiment analysis expert. Provide detailed analysis including emotion, tone, and confidence score."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200
            )
            
            return response['choices'][0]['message']['content']
            
        except Exception as e:
            return f"Sentiment analysis error: {str(e)}"
    
    def translate_text(self, text, target_language):
        """Translate text using AI"""
        try:
            prompt = f"Translate this text to {target_language}: {text}"
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a professional translator. Translate the given text to {target_language}."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300
            )
            
            return response['choices'][0]['message']['content']
            
        except Exception as e:
            return f"Translation error: {str(e)}"
    
    def summarize_text(self, text, max_length="medium"):
        """Summarize text using AI"""
        try:
            length_map = {
                "short": "2-3 sentences",
                "medium": "4-6 sentences", 
                "long": "8-10 sentences"
            }
            
            prompt = f"Summarize this text in {length_map.get(max_length, '4-6 sentences')}: {text}"
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional summarizer. Create clear, concise summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300
            )
            
            return response['choices'][0]['message']['content']
            
        except Exception as e:
            return f"Summarization error: {str(e)}"
    
    def code_assistant(self, code_or_request):
        """AI-powered code assistant"""
        try:
            prompt = f"""
            You are an expert programmer. Help with this code or request:
            {code_or_request}
            
            Provide:
            1. Code solution or improvement
            2. Explanation
            3. Best practices
            4. Potential issues to watch for
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert programmer specializing in Python, JavaScript, and general software development."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800
            )
            
            return response['choices'][0]['message']['content']
            
        except Exception as e:
            return f"Code assistant error: {str(e)}"
    
    def voice_to_text(self, audio_file_path):
        """Convert voice to text using Whisper"""
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = openai.Audio.transcribe(
                    "whisper-1",
                    audio_file
                )
            
            return transcript['text']
            
        except Exception as e:
            return f"Voice-to-text error: {str(e)}"
    
    def text_to_speech(self, text, voice="alloy"):
        """Convert text to speech using OpenAI TTS"""
        try:
            response = openai.Audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text
            )
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tts_output_{timestamp}.mp3"
            
            with open(filename, "wb") as f:
                f.write(response.content)
            
            return f"Speech saved as {filename}"
            
        except Exception as e:
            return f"Text-to-speech error: {str(e)}"
    
    def smart_reminder(self, task_description):
        """AI-powered smart reminder with context understanding"""
        try:
            prompt = f"""
            Analyze this task and create a smart reminder:
            Task: {task_description}
            
            Provide:
            1. Priority level (high/medium/low)
            2. Suggested deadline
            3. Related tasks or dependencies
            4. Best time to work on this
            5. Required resources or tools
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a productivity expert. Help create smart, contextual reminders."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300
            )
            
            return response['choices'][0]['message']['content']
            
        except Exception as e:
            return f"Smart reminder error: {str(e)}"
    
    def ai_research(self, topic):
        """AI-powered research assistant"""
        try:
            prompt = f"""
            Research this topic comprehensively:
            Topic: {topic}
            
            Provide:
            1. Key points and facts
            2. Recent developments
            3. Different perspectives
            4. Related topics
            5. Sources and references (if applicable)
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a research expert. Provide comprehensive, well-structured research on any topic."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800
            )
            
            return response['choices'][0]['message']['content']
            
        except Exception as e:
            return f"Research error: {str(e)}"
    
    def conversation_analysis(self):
        """Analyze conversation history for insights"""
        try:
            if not self.conversation_history:
                return "No conversation history to analyze."
            
            # Get recent conversation
            recent_messages = self.conversation_history[-20:]
            conversation_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in recent_messages])
            
            prompt = f"""
            Analyze this conversation and provide insights:
            {conversation_text}
            
            Provide:
            1. Main topics discussed
            2. User's interests and patterns
            3. Areas where assistance was most needed
            4. Suggestions for improvement
            5. Conversation quality assessment
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a conversation analyst. Provide insights about user interactions and patterns."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400
            )
            
            return response['choices'][0]['message']['content']
            
        except Exception as e:
            return f"Conversation analysis error: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        return "Conversation history cleared."
    
    def get_ai_status(self):
        """Get AI system status"""
        return {
            "current_context": self.current_context,
            "conversation_length": len(self.conversation_history),
            "available_models": list(self.models.keys()),
            "available_contexts": list(self.contexts.keys())
        }

# Global instance
enhanced_ai = EnhancedAI()

def get_enhanced_ai():
    """Get the global enhanced AI instance"""
    return enhanced_ai 