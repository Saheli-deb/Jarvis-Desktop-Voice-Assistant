# gesture.py

import cv2
import mediapipe as mp
import pyautogui
import time
from ultralytics import YOLO  # YOLOv8

# Initialize MediaPipe modules
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose
mp_face = mp.solutions.face_detection
mp_draw = mp.solutions.drawing_utils

# Load YOLOv8 pre-trained model
yolo_model = YOLO("yolov8n.pt")  # Use yolov8s.pt or yolov8m.pt for higher accuracy

def detect_gestures():
    cap = cv2.VideoCapture(0)
    hands = mp_hands.Hands(min_detection_confidence=0.7)
    pose = mp_pose.Pose()
    face_detection = mp_face.FaceDetection(model_selection=1, min_detection_confidence=0.5)

    prev_y = None
    gesture_trigger_time = time.time()

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # HAND DETECTION
        hand_results = hands.process(rgb)
        if hand_results.multi_hand_landmarks:
            for hand_landmark in hand_results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmark, mp_hands.HAND_CONNECTIONS)

                y = hand_landmark.landmark[8].y  # Index finger tip
                h, w, _ = frame.shape
                cy = int(y * h)

                if prev_y is not None:
                    dy = prev_y - cy
                    if dy > 20 and time.time() - gesture_trigger_time > 1:
                        pyautogui.scroll(400)
                        print("🖱️ Scroll Up Gesture Detected")
                        gesture_trigger_time = time.time()
                    elif dy < -20 and time.time() - gesture_trigger_time > 1:
                        pyautogui.scroll(-400)
                        print("🖱️ Scroll Down Gesture Detected")
                        gesture_trigger_time = time.time()

                prev_y = cy

        # POSE DETECTION
        pose_results = pose.process(rgb)
        if pose_results.pose_landmarks:
            mp_draw.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            print("🧍 Body Detected")

        # FACE DETECTION
        face_results = face_detection.process(rgb)
        if face_results.detections:
            for detection in face_results.detections:
                mp_draw.draw_detection(frame, detection)
            print("🧠 Face Detected")

        # YOLO OBJECT DETECTION
        results = yolo_model.predict(source=frame, conf=0.5, save=False, verbose=False)

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls_id = int(box.cls[0])
                label = yolo_model.names[cls_id]
                conf = box.conf[0]

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("🖐️ Gesture & YOLO Vision", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
