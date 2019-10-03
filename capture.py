import numpy as np
import cv2
import time
from robot import Robot

def vision():
    Width = 640.
    Height = 480.

    robot = Robot()

    video_capture = cv2.VideoCapture(0)
    video_capture.set(3, Width)
    video_capture.set(4, Height)

    i = 0
    transition = False

    while(i<3):
        print(time.clock())
        ret,frame = video_capture.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        # cv2.imshow('frame',hsv)
        #cv2.waitKey(1)

        lower = np.array(np.matrix([[20,50,50],[80,100,100],[0,39,64],[110,50,50]]))
        upper = np.array(np.matrix([[60,200,200],[105,255,255],[20,255,255],[130,255,255]]))

        mask_jaune = cv2.inRange(hsv,lower[1], upper[1])  # jaune
        mask_bleu = cv2.inRange(hsv,lower[2], upper[2])  # bleu
        mask_rouge = cv2.inRange(hsv,lower[3], upper[3])  # rouge
        mask_couleur= list((mask_jaune, mask_bleu, mask_rouge))


        mask_vert = cv2.inRange(hsv,lower[0], upper[0]) # creation du mask vert hsv
        res1 = cv2.bitwise_and(frame,frame, mask= mask_vert) # masque vert case depart


        mask = mask_vert + mask_couleur[i]
        res = cv2.bitwise_and(frame,frame,mask= mask)
        difference_moyenne = np.mean(mask_vert)-np.mean(mask_couleur[i])  #difference de moyenne
        print("mask_vert", np.mean(mask_vert), "mask_",i, np.mean(mask_couleur[i]))
        print(i, "diff moy", difference_moyenne)

        if difference_moyenne  <= 0:  # le vert domine pas
            transition = False
            robot.baseSpeed -= 20
            print("suivre la ligne")
        else:
            if (difference_moyenne > 0) and (transition == False):
                transition = True
                # t_transition = time.clock()
                robot.baseSpeed += 20
                robot.move_straight_forward(robot.baseSpeed)
                i = (i+1)
                print("changement de ligne")


        gray_image = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)  # conversion de l image en niveau de gris
        ret,thresh = cv2.threshold(gray_image,127,255,0)  # binarisation

        M = cv2.moments(thresh)  # detecter la ligne

        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])  #coordonnees du centre en x
            cY = int(M["m01"] / M["m00"])  #coordonnees du centre en y

        else :
            cX, cY = 0, 0

        #print(cX)
        #print(cY)
        cv2.circle(res, (cX, cY), 5, (255, 255, 255), -1)
        cv2.putText(res, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        delta = (1/Width) * ( Width/2-cX)

        #print(delta)

        if delta  >= 0.15:
            print("le robot doit tourner a gauche")
            robot.move(-Robot.baseSpeed*0.6 , -Robot.baseSpeed*0.6 - Robot.coeff*delta)
        elif delta  <= -0.15:
            print("le robot doit tourner a droite")
            robot.move(Robot.baseSpeed*0.6 + Robot.coeff*delta, Robot.baseSpeed*0.6)
        else:
            print("le robot avance tout droit")
            robot.move(Robot.baseSpeed, -Robot.baseSpeed)

        # affichage de l image

        # cv2.imshow('frame',frame)
        # cv2.imshow('mask',mask)
        # cv2.imshow('res',res)
        k = cv2.waitKey(5) & 0xFF
        if k == 35:
            break

    robot.stop()
    cv2.destroyAllWindows()
