import cv2
import mediapipe as mp
import time

engine = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
draw = mp.solutions.drawing_utils

prev_time = 0

while True:
    success, image = engine.read()

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for i in results.multi_hand_landmarks:
            for idx, lm in enumerate(i.landmark):
                print(idx, lm)
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)
                if idx == 0:
                    cv2.circle(image, (cx, cy), 25, (255, 0, 255))

            draw.draw_landmarks(image, i, mpHands.HAND_CONNECTIONS)

    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time
    cv2.putText(image, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX,
                3, (255, 0, 0), 2)

    cv2.imshow("Image", image)
    cv2.waitKey(1)
