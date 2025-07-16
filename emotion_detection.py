# emotion_detection.py
import cv2
from deepface import DeepFace
import numpy as np
import librosa
import sounddevice as sd
import tempfile
import os
from pygame import mixer

# Initialize sound mixer for alerts
mixer.init()

def detect_face_emotion():
    """Detects emotion from facial expression using webcam."""
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    
    emotion = "neutral"
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face = frame[y:y+h, x:x+w]
                result = DeepFace.analyze(face, actions=['emotion'], enforce_detection=False)
                emotion = result[0]['dominant_emotion']
                
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(frame, f"Emotion: {emotion}", (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

            cv2.imshow('Emotion Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q') or emotion != "neutral":
                break

    except Exception as e:
        print(f"[FACE ERROR] {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        return emotion

def record_voice(duration=3, sample_rate=22050):
    """Records audio snippet from microphone."""
    print("\nListening for voice tone...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    temp_file = tempfile.mktemp(suffix=".wav")
    librosa.output.write_wav(temp_file, audio.flatten(), sample_rate)
    return temp_file

def analyze_voice_emotion(audio_path):
    """Analyzes voice tone for stress/sadness."""
    try:
        y, sr = librosa.load(audio_path)
        pitch = librosa.yin(y, fmin=50, fmax=500)
        intensity = np.mean(librosa.feature.rms(y=y))
        
        if np.nanmean(pitch) > 180:
            return "stressed"
        elif intensity < 0.01:
            return "sad"
        else:
            return "neutral"
    except Exception as e:
        print(f"[VOICE ERROR] {e}")
        return "neutral"

def get_combined_emotion():
    """Combines face and voice analysis for robust emotion detection."""
    face_emotion = detect_face_emotion()
    voice_file = record_voice()
    voice_emotion = analyze_voice_emotion(voice_file)
    os.remove(voice_file)

    # Decision logic
    if face_emotion == voice_emotion:
        return face_emotion
    elif face_emotion != "neutral":
        return face_emotion
    else:
        return voice_emotion

def play_emotion_response(emotion):
    """Plays appropriate response based on detected emotion."""
    if emotion == "sad":
        mixer.music.load("calm_music.mp3")  # Add your sound file
        mixer.music.play()
        return "Playing calming music..."
    elif emotion == "angry":
        return "Try taking deep breaths. Would you like me to dim the lights?"
    else:
        return None