import cv2
import face_recognition
import pyttsx3
import time

# Load stored face data
known_image = face_recognition.load_image_file("user_face.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]

engine = pyttsx3.init("sapi5")
engine.setProperty("voice", engine.getProperty("voices")[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def face_login():
    """Activate Jarvis only when user's face is detected"""
    cap = cv2.VideoCapture(0)

    speak("Scanning for face recognition. Please look at the camera.")
    time.sleep(2)  # Delay for user preparation

    while True:
        ret, frame = cap.read()
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces([known_encoding], face_encoding)
            if True in matches:
                speak("Face recognized. Jarvis is now active.")
                cap.release()
                cv2.destroyAllWindows()
                return True  # Jarvis activation success

        cv2.imshow("Face Recognition Login", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Quit with 'q' key
            break

    cap.release()
    cv2.destroyAllWindows()
    return False  # If no match found
