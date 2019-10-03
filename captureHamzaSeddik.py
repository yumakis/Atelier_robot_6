import numpy as np
import cv2
from robot import Robot

Width = 640.
Height = 480.

robot = Robot()

video_capture = cv2.VideoCapture(0)
video_capture.set(3, Width)
video_capture.set(4, Height)

while(True):
    ret,frame = video_capture.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    cv2.imshow("frame",hsv)
    #cv2.waitKey(1)

    #vert jaune bleu rouge
    lower = np.array(np.matrix([[30,100,100],[80,100,100],[0,39,64],[110,50,50]]))
    upper = np.array(np.matrix([[70,255,255],[105,255,255],[20,255,255],[130,255,255]]))


    mask = cv2.inRange(hsv,lower[2], upper[2])

    res = cv2.bitwise_and(frame,frame, mask=mask) # Application du mask sur la frame pour segmenter

    gray_image = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)  # conversion de l image en niveau de gris
    ret,thresh = cv2.threshold(gray_image,127,255,0)  # binarisation

    M = cv2.moments(thresh)  # detecter la ligne

    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])  #coordonnees du centre en x
        cY = int(M["m01"] / M["m00"])  #coordonnees du centre en y

    else :
        cX, cY = 0, 0

    print(cX)
    print(cY)
    cv2.circle(res, (cX, cY), 5, (255, 255, 255), -1)
    cv2.putText(res, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    delta = (1/Width) * ( Width/2-cX)

    print(delta)

    if(delta  >= 0.1): #on tourne a gauche
        robot.move(-Robot.baseSpeed + Robot.coeff*delta, -Robot.baseSpeed - Robot.coeff*delta)
    elif(delta  <= -0.1):
        robot.move(Robot.baseSpeed + Robot.coeff*delta, Robot.baseSpeed - Robot.coeff*delta)

    # affichage de l image

    #cv2.imshow("frame",frame)
    #cv2.imshow("mask",mask)
    #cv2.imshow("res",res)
    k = cv2.waitKey(5) & 0xFF
    if k == 35:
        break

cv2.destroyAllWindows()
