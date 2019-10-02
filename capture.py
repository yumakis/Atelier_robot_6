import numpy as np
import cv2


video_capture = cv2.VideoCapture(0)
video_capture.set(3, 340)
video_capture.set(4, 480)

countGreenStart = 0


while(True and countGreenStart <= 3):

    ret,frame = video_capture.read()
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
   
    cv2.imshow('frame',hsv)
    #cv2.waitKey(1)

    lower_blue = np.uint8([0,39,64])
    upper_blue = np.uint8([20,255,255])

    lower_red = np.uint8([50,50,100])
    upper_red = np.uint8([255,255,130])
    
    lower_green = np.uint8([41, 39, 64])
    upper_green = np.uint8([80, 255, 255])

    lower_yellow = np.uint8([10,0,100])
    upper_yellow = np.uint8([40,170,255])

    lower_range = np.uint8([0, 80, 0])
    upper_range = np.uint8([255, 255, 255])

    mask = cv2.inRange(hsv,lower_red, upper_red)

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
    res = cv2.bitwise_and(frame,frame, mask= mask)
    # Get the line center
    
    
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()