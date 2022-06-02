import cv2
import time
import math
import handTracker
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc

engine = cv2.VideoCapture(0)
w_cam, h_cam = 640, 480
engine.set(3, w_cam)
engine.set(4, h_cam)

detector = handTracker.HandDetector()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
min_volume, max_volume, *_ = volume.GetVolumeRange()


def main():
    while True:
        success, image = engine.read()
        image = detector.locateHands(image)
        ls = detector.getPosition(image, draw=False)
        vol_bar = 0
        if len(ls) > 0:
            fingers_landmark = [4, 8]  # Tip of Thumb and Index finger
            x1, y1 = ls[fingers_landmark[0]][1], ls[fingers_landmark[0]][2]
            x2, y2 = ls[fingers_landmark[1]][1], ls[fingers_landmark[1]][2]

            distance = np.hypot(x2 - x1, y2 - y1)
            vol_bar = np.interp(distance, [50, 300], [400, 150])
            if ls[4][1] < ls[20][1]:
                # Brightness
                x1, y1 = ls[4][1], ls[4][2]
                x2, y2 = ls[8][1], ls[8][2]
                x3, y3 = ls[12][1], ls[12][2]
                x4, y4 = ls[16][1], ls[16][2]
                x5, y5 = ls[20][1], ls[20][2]

                list1 = [x2, x3, x4, x5]
                list2 = [y2, y3, y4, y5]
                len1 = []
                for i, j in zip(list1, list2):
                    l1 = math.hypot(i - x1, j - y1)
                    len1.append(l1)

                m1 = math.hypot(x3 - x2, y3 - y2)
                m2 = math.hypot(x4 - x3, y4 - y3)
                m3 = math.hypot(x5 - x4, y5 - y4)
                len2 = [m1, m2, m3, 0]
                area = 0
                flag = 0
                k = 0
                for i, j in zip(len1, len2):
                    k = k + 1
                    if flag == 3:
                        break
                    s = (i + j + len1[k]) // 2
                    p = math.sqrt(s * int(s - i) * int(s - j) * int(s - len1[k]))
                    area = area + p
                    flag = flag + 1
                val = np.interp(area, [300, 30000], [0, 100])
                sbc.set_brightness(int(val))
            else:
                # Volume
                cv2.circle(image, (x1, y1), 15, (255, 0, 0))
                cv2.circle(image, (x2, y2), 15, (255, 0, 0))

                cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255))
                # cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                # cv2.circle(image, (cx, cy), 15, (255, 0, 0))
                val = np.interp(distance, [50, 200], [min_volume, max_volume])
                volume.SetMasterVolumeLevel(val, None)

        # cv2.rectangle(image, (50, 150), (35, 400), (8, 255, 0))
        # cv2.rectangle(image, (50, max(int(vol_bar), 150)), (35, 400), (8, 255, 0), cv2.FILLED)

        cv2.imshow('Image', image)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()
