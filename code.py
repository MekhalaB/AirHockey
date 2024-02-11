import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Importing all images
imgBackground = cv2.imread("AHResources/table2.png")
imgGameOver = cv2.imread("AHResources/gameOver.png")
imgPuck = cv2.imread("AHResources/puck.png", cv2.IMREAD_UNCHANGED)
imgPaddle1 = cv2.imread("AHResources/bat1.png", cv2.IMREAD_UNCHANGED)
imgPaddle2 = cv2.imread("AHResources/bat2.png", cv2.IMREAD_UNCHANGED)
imgGoal = cv2.imread("AHResources/goal.png", cv2.IMREAD_UNCHANGED)

# Variables
puckPos = [160, 50]
speedX = 20
speedY = 20
gameOver = False
score = [0, 0]

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=2)

while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)
    imgRaw = img.copy()

    # Find the hand and its landmarks
    hands, img = detector.findHands(img, flipType=False)  # with draw

    # Overlaying the background image
    img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0)

    #check for hands
    if hands:
        for hand in hands:
            x, y, w, h = hand['bbox']
            h1, w1, _ = imgPaddle1.shape
            y1 = y - h1 // 2
            x1 = x-w1//2
            x2 = x-w1//2
            y1 = np.clip(y1, 45, 425)
            x1 = np.clip(x1, 150, 615)
            x2 = np.clip(x2, 640, 1100)

            if hand['type'] == "Left":
                img = cvzone.overlayPNG(img, imgPaddle1, (x1, y1))
                if x1 < puckPos[0] < x1 + w1 and y1 < puckPos[1] < y1 + h1:
                    speedX = -speedX
                    puckPos[0] +=30
                if x1 - w1 < puckPos[0] < x1 and y1 < puckPos[1] < y1 + h1:
                    speedX = -speedX
                    puckPos[0] -= 30


            if hand['type'] == "Right":
                img = cvzone.overlayPNG(img, imgPaddle2, (x2, y1))
                if x2 < puckPos[0] < x2 + w1 and y1 < puckPos[1] < y1 + h1:
                    speedX = -speedX
                    puckPos[0] += 30
                if x2 - w1 < puckPos[0] < x2 and y1 < puckPos[1] < y1 + h1:
                    speedX = -speedX
                    puckPos[0] -= 30


    #Game Over
    if score[0]==10 or score[1]==10:
        gameOver=True

    if gameOver:
        img = imgGameOver


    #if game not over, move ball
    else:
       #Move the Puck
        if puckPos[1] >= 475 or puckPos[1] <= 40:
            speedY = -speedY
        if puckPos[0] >= 1075 or puckPos[0] <= 150:
            speedX= -speedX
        #score for left side
        if puckPos[0] >= 1074 and (puckPos[1] >= 45 or puckPos[1] <= 425):
            score[0] += 1
        #score for right side
        if puckPos[0] <=152 and (puckPos[1] >= 45 or puckPos[1] <= 425):
            score[1] += 1


        cv2.putText(img, str(score[0]), (300, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
        cv2.putText(img, str(score[1]), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)

        puckPos[0] += speedX
        puckPos[1] += speedY

       # Draw Puck
        img = cvzone.overlayPNG(img, imgPuck, puckPos)


    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('r'):
        ballPos = [100, 100]
        speedX = 15
        speedY = 15
        gameOver = False
        score = [0, 0]
        imgGameOver = cv2.imread("Resources/gameOver.png")
