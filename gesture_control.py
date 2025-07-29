# gesture_control.py
import cv2
import mediapipe as mp
import pyautogui
import time

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

def count_fingers(hand_landmarks):
    fingers = []

    tipIds = [4, 8, 12, 16, 20]

    # Thumb
    if hand_landmarks.landmark[tipIds[0]].x < hand_landmarks.landmark[tipIds[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Fingers
    for id in range(1, 5):
        if hand_landmarks.landmark[tipIds[id]].y < hand_landmarks.landmark[tipIds[id] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)

def start_gesture_control():
    cap = cv2.VideoCapture(0)
    prev_action_time = 0

    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
                finger_count = count_fingers(handLms)

                current_time = time.time()

                if current_time - prev_action_time > 2:  # delay to avoid rapid triggering
                    if finger_count == 1:
                        pyautogui.press("k")  # Play/Pause
                        print("Play/Pause")
                    elif finger_count == 2:
                        pyautogui.press("volumeup")
                        print("Volume Up")
                    elif finger_count == 3:
                        pyautogui.press("volumedown")
                        print("Volume Down")
                    elif finger_count == 4:
                        pyautogui.scroll(200)
                        print("Scroll Up")
                    elif finger_count == 5:
                        pyautogui.scroll(-200)
                        print("Scroll Down")
                    prev_action_time = current_time

        cv2.imshow("Gesture Control", img)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
