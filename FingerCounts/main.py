# Import libraries
import cv2
import mediapipe as mp

# Initialize MediaPipe Hands and Drawing
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,  # Live video feed
                       max_num_hands=1,          # Only one hand detected allows
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Define IDs for tip landmark for thumb to pinky
finger_tips = [4, 8, 12, 16, 20]

# Open webcam, force it to a higher resolution (e.g. 960x720)
video_capture = cv2.VideoCapture(0)
# Using 720p since 1080p is too big
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# 1st helper function (Detect hands)
def find_hands(img, draw=True):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            if draw:
                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    return img, results

# 2nd helper function (Get landmark positions)
def find_position(img, results, hand_no=0, draw=True):
    lm_list = []
    if results.multi_hand_landmarks:
        my_hand = results.multi_hand_landmarks[hand_no]
        for id, lm in enumerate(my_hand.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lm_list.append([id, cx, cy])
            if draw:
                cv2.circle(img, (cx, cy), 6, (255, 0, 255), cv2.FILLED)
    return lm_list

# A loop to keep the program running (real-time processing)
while True:
    success, frame = video_capture.read()
    if not success:
        print("Error: webcam.")
        break

    # Draw a centering 300x300 pixel green box
    h, w, _ = frame.shape
    box_size = 300
    x1 = w // 2 - box_size // 2
    y1 = h // 2 - box_size // 2
    x2 = x1 + box_size
    y2 = y1 + box_size
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Detect hand and get landmarks for fingers
    frame, results = find_hands(frame)
    landmarks = find_position(frame, results, draw=True)

    if len(landmarks) != 0:
        wrist_x, wrist_y = landmarks[0][1], landmarks[0][2]

        # Check wrist is inside the center box (it needs to!!!)
        if x1 < wrist_x < x2 and y1 < wrist_y < y2:
            fingers_status = []

            # Check the thumb: compare x position (left vs right direction)
            if landmarks[finger_tips[0]][1] > landmarks[finger_tips[0] - 1][1]:
                fingers_status.append(1)
            else:
                fingers_status.append(0)

            # Check other fingers: compare y position (bent vs straight)
            for i in range(1, 5):
                if landmarks[finger_tips[i]][2] < landmarks[finger_tips[i] - 2][2]:
                    fingers_status.append(1)
                else:
                    fingers_status.append(0)

            total_fingers_up = sum(fingers_status)

            # Draw number in the upper right corner correspond to finger displaying inside the green box
            cv2.rectangle(frame, (w - 120, 10), (w - 20, 70), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, str(total_fingers_up), (w - 100, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4)

    # Display the output frame
    cv2.imshow("Finger Counter", frame)

    # Quit on a 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup the program
video_capture.release()
cv2.destroyAllWindows()