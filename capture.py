import numpy as np
import cv2
#from robot import Robot

WIDTH = 640
HEIGHT = 480

#robot = Robot()

video_capture = cv2.VideoCapture(0)
video_capture.set(3, WIDTH)
video_capture.set(4, HEIGHT)

countGreenStart = 0

while(True and countGreenStart < 3):
    #capture image
    ret,frame = video_capture.read()
    #crop image
    crop_img = frame[379:480, 0:640]

    hsv = cv2.cvtColor(crop_img, cv2.COLOR_RGB2HSV)

    #lower_blue = np.uint8([0,39,64])
    #upper_blue = np.uint8([20,255,255])

    #lower_red = np.uint8([50,50,100])
    #upper_red = np.uint8([255,255,130])
    
    #lower_green = np.uint8([41, 39, 64])
    #upper_green = np.uint8([80, 255, 255])

    #lower_yellow = np.uint8([10,0,100])
    #upper_yellow = np.uint8([40,170,255])

    lower = np.array(np.matrix([[30,100,100],[80,100,100],[0,39,64],[110,50,50]]))
    upper = np.array(np.matrix([[70,255,255],[105,255,255],[20,255,255],[130,255,255]]))

    #lower_range = np.uint8([0, 80, 0])
    #upper_range = np.uint8([255, 255, 255])

    mask = cv2.inRange(hsv,lower[countGreenStart], upper[countGreenStart])

    # Remove noise
    #kernel_erode = np.ones((4,4), np.uint8)
    #eroded_mask = cv2.erode(mask, kernel_erode, iterations=1)
    #kernel_dilate = np.ones((6,6), np.uint8)
    #dilated_mask = cv2.dilate(eroded_mask, kernel_dilate, iterations=1)  #Dilatation
    # Find the different contours
    #contours, hierarchy = cv2.findContours(dilated_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Sort by area (keep only the biggest one)
    #contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]
    #if len(contours) > 0:
    #    M = cv2.moments(contours[0])
        # Centroid
    #    cx = int(M['m10']/M['m00'])
    #    cy = int(M['m01']/M['m00'])
    #    print("Centroid of the biggest area: ({}, {})".format(cx, cy))
    #else:
    #    print("No Centroid Found")
    res = cv2.bitwise_and(crop_img,crop_img, mask= mask)
    # Get the line center
    
    gray_image = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)  # conversion de l image en niveau de gris
    ret,thresh = cv2.threshold(gray_image,127,255,0)  # binarisation

    contours, hierarchy = cv2.findContours(thresh.copy(),1, cv2.CHAIN_APPROX_NONE)

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        if int(M['m00']) == 0:
            continue

    M = cv2.moments(thresh)  # detecter la ligne
        
        
    cX = int(M["m10"] / M["m00"])  #coordonnees du centre en x
    cY = int(M["m01"] / M["m00"])  #coordonnees du centre en y
    print(cX, cY)
    cv2.circle(res, (cX, cY), 5, (255, 255, 255), -1)
    cv2.putText(res, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)

    # cx = int(M['m10']/M['m00'])
    # cy = int(M['m01']/M['m00'])

    #delta = Robot.coef * (cx - WIDTH/2)
    #robot.move(Robot.baseSpeed + delta, Robot.baseSpeed - delta)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()