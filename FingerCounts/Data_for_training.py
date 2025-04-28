# Import libraries
import cv2
import mediapipe as mp
import csv
import os

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Create a data folder to store collected data if not exist
os.makedirs("data", exist_ok=True)
csv_path = "data/landmarks.csv"

# Open CSV for writing the collected data
file = open(csv_path, 'a', newline='')
csv_writer = csv.writer(file)

# Header row in CSV (only if new file created)
if os.stat(csv_path).st_size == 0:
    headers = [f"{coord}_{i}" for i in range(21) for coord in ['x', 'y', 'z']] + ['label']
    csv_writer.writerow(headers)

# Open webcam
cap = cv2.VideoCapture(0)
print("Press 1-5 on keyboard to label the number of fingers, 'q' to quit.")

# A loop to keep the program running
while True:
    success, frame = cap.read()
    if not success:
        break

    h, w, c = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Data Collector - Press 1-5 to label", frame)
    key = cv2.waitKey(1) & 0xFF

    # Save landmarks only when a number key is pressed
    if ord('1') <= key <= ord('5'):
        label = key - ord('0')  # Convert to int
        print(f"Captured label: {label}")

        hand_landmarks = results.multi_hand_landmarks[0]
        row = []
        for lm in hand_landmarks.landmark:
            row.extend([lm.x, lm.y, lm.z])
        row.append(label)
        csv_writer.writerow(row)

    elif key == ord('q'):
        break

# Cleanup the program
cap.release()
file.close()
cv2.destroyAllWindows()
