import cv2
import mediapipe as mp
# mp_drawing = mp.solutions.drawing_utils
# mp_drawing_styles = mp.solutions.drawing_styles
# mphands = mp.solutions.hands

# cap = cv2.VideoCapture(0)
# hands = mphands.Hands()

def findPosition(img, results , handNo=0, draw=True):
        xList = []
        yList = []
        bbox = []
        lmList = []
        if results.multi_hand_landmarks:
            myHand = results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        xmin, xmax = min(xList), max(xList)
        ymin, ymax = min(yList), max(yList)
        bbox = xmin, ymin, xmax, ymax

        if draw:
            cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),
            (0, 255, 0), 2)

        return lmList, bbox
    
def fingersUp(lmList , tipIds):
        fingers = []
        # Thumb
        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

            # totalFingers = fingers.count(1)

        return fingers
# while True:
#     data , image = cap.read()
#     image = cv2.cvtColor(cv2.flip(image,1),cv2.COLOR_BGR2RGB)
#     results = hands.process(image)
#     image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             mp_drawing.draw_landmarks(
#                 image,
#                 hand_landmarks,mphands.HAND_CONNECTIONS)
#     cv2.imshow("Image",image)
#     cv2.waitKey(1)