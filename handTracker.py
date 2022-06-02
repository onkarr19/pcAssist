import cv2
import mediapipe as mp


class HandDetector:
    def __init__(self, mode=False, max_hands=1, model_complexity=1, detection_confidence=0.5, track_confidence=0.5):
        self.results = None
        self.mode = mode
        self.maxHands = max_hands
        self.modelComplex = model_complexity
        self.detectionCon = detection_confidence
        self.trackCon = track_confidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex,
                                        self.detectionCon, self.trackCon)
        self.draw = mp.solutions.drawing_utils

    def locateHands(self, image, draw=True):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(image_rgb)

        if self.results.multi_hand_landmarks:
            for i in self.results.multi_hand_landmarks:
                if draw:
                    self.draw.draw_landmarks(image, i, self.mpHands.HAND_CONNECTIONS)

        return image

    def getPosition(self, image, hand_no=0, draw=True):
        ls = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[hand_no]
            for idx, lm in enumerate(hand.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                ls.append([idx, cx, cy])
                if draw:
                    cv2.circle(image, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return ls


def main():
    return


if __name__ == '__main__':
    main()
