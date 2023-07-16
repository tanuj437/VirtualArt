import os
import cv2
import mediapipe as mp
import numpy as np
from Handtracker import *

#Selection is done with two fingers (index and middle)
#Drawing is done with index finger only

######################
brushthickness = 3
eraserthickness = 50
xp , yp = 0,0
######################

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mphands = mp.solutions.hands
hands = mphands.Hands()
cap = cv2.VideoCapture(0)
tipIds = [4, 8, 12, 16, 20]

folderpath = "header"
myList = os.listdir(folderpath)
# print(myList)
overlayList = []
for imgpath in myList:
    image = cv2.imread(f'{folderpath}/{imgpath}')
    overlayList.append(image)
# print(len(overlayList))

header = overlayList[0]
drawcolor = (14,198,255)
cap.set(3,640)
cap.set(4,720)

imgcanvas = np.zeros((720,640,4),np.uint8)
while True:
    #2) Find hand landmarks
    data, image = cap.read()
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    #print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks, mphands.HAND_CONNECTIONS)
    
    if results.multi_hand_landmarks != None:
        lmList , bbox = findPosition(image,results,draw=True)
        
        if len(lmList)!=0:
            #print(lmList)
            
            #tip of index hand middle finger
            x1,y1 = lmList[8][1:]
            x2,y2 = lmList[12][1:]
            
            #3) checking which fingers are up
            fingers = fingersUp(lmList,tipIds)
            #print(fingers)
            
            #4) selection with 2 fingers up
            if fingers[1] and fingers[2]:
                xp , yp = 0,0
                print("Selection Mode")
                if y1<120:
                    if 197<x1<210:
                        header = overlayList[0]
                        drawcolor = (14,198,255)
                    elif 230<x1<320:
                        header = overlayList[1]
                        drawcolor = (190,107,253)
                    elif 369<x1<440:
                        header = overlayList[2]
                        drawcolor = (102,205,0)
                    elif 454<x1<525:
                        header = overlayList[3]
                        drawcolor = (0,0,255)
                    elif 545<x1<630:
                        header = overlayList[4]
                        drawcolor = (0,0,0)
                cv2.rectangle(image, (x1, y1), (x2, y2), drawcolor, cv2.FILLED)
                        
            #5) drawing with one finger up
            if fingers[1] and fingers[2]==False:
                cv2.circle(image, (x1, y1), 5, drawcolor, cv2.FILLED)
                print("Drawing Mode")
                if xp == 0 and yp == 0:
                    xp , yp = x1,x2  
                    
                if drawcolor == (0,0,0):
                    cv2.line(image,(xp,yp),(x1,y1),drawcolor,eraserthickness)
                    cv2.line(imgcanvas,(xp,yp),(x1,y1),drawcolor,eraserthickness)
                 
                else:   
                    cv2.line(image,(xp,yp),(x1,y1),drawcolor,brushthickness)
                    cv2.line(imgcanvas,(xp,yp),(x1,y1),drawcolor,brushthickness)
                
                xp , yp = x1,y1
                
    # imgGray = cv2.cvtColor(imgcanvas,cv2.COLOR_BGR2GRAY)
    # _,imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    # imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    # image = cv2.bitwise_and(image,imgInv)
    # image = cv2.bitwise_or(image,imgcanvas)
                
    # Setting the header image
    image[0:120, 0:640] = header
    #image = cv2.addWeighted(image,0.5,imgcanvas,0.5,0)
    cv2.imshow("Image", image)
    cv2.imshow("Canvas", imgcanvas)
    # cv2.imshow("Inv", imgInv)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    
    cv2.waitKey(1) 
cap.release()
cv2.destroyAllWindows()
