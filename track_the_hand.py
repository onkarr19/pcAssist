import cv2
import time
import handTracker as ht

engine = cv2.VideoCapture(0)
prev_time = 0
detector = ht.HandDetector()

while True:
    success, image = engine.read()
    image = detector.locateHands(image)
    ls = detector.getPosition(image)
    if len(ls) > 0:
        print(ls)

    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    cv2.putText(image, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX,
                3, (255, 0, 0), 2)
    cv2.imshow("Image", image)
    cv2.waitKey(1)
