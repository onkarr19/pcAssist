import cv2
import time
import handTracker
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

engine = cv2.VideoCapture(0)
w_cam, h_cam = 640, 480
engine.set(3, w_cam)
engine.set(4, h_cam)

detector = handTracker.HandDetector()

prev_time = 0
fingers_landmark = [4, 8]

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumelevel()
min_volume, max_volume, *_ = volume.GetVolumeRange()
volume.SetMasterVolumeLevel(-20.0, None)

try:

    while True:
        success, image = engine.read()
        image = detector.locateHands(image)
        ls = detector.getPosition(image, draw=False)
        vol = 0
        vol_bar = 0
        if len(ls) > 0:
            # print(ls[2])

            x1, y1 = ls[fingers_landmark[0]][1], ls[fingers_landmark[0]][2]
            x2, y2 = ls[fingers_landmark[1]][1], ls[fingers_landmark[1]][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            cv2.circle(image, (x1, y1), 15, (255, 0, 0))
            cv2.circle(image, (x2, y2), 15, (255, 0, 0))

            cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255))
            cv2.circle(image, (cx, cy), 15, (255, 0, 0))

            distance = np.hypot(x2 - x1, y2 - y1)
            # print(distance)

            vol = np.interp(distance, [50, 300], [min_volume, max_volume])
            vol_bar = np.interp(distance, [50, 300], [400, 150])
            print(distance, vol)
            volume.SetMasterVolumeLevel(vol, None)

            if distance < 50:
                cv2.circle(image, (cx, cy), 15, (255, 0, 255))

        cv2.rectangle(image, (50, 150), (35, 400), (8, 255, 0))
        cv2.rectangle(image, (50, max(int(vol_bar), 150)), (35, 400), (8, 255, 0), cv2.FILLED)
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time

        cv2.putText(image, f'FPS: {str(int(fps))}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 0, 0), 2)

        cv2.imshow('Image', image)
        cv2.waitKey(1)

except KeyboardInterrupt as error:
    print('process ended')