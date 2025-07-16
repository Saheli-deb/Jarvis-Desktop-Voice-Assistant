import cv2
from deepface import DeepFace
from ultralytics import YOLO
import face_recognition

def detect_faces():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow("Face Detection", frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def detect_objects():
    model = YOLO("yolov8n.pt")
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        model.predict(source=frame, show=True)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def detect_emotion():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        results = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
        print("Detected Emotion:", results[0]['dominant_emotion'])
        cv2.imshow("Emotion Detection", frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
