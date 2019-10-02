import numpy as np
import cv2


video_capture = cv2.VideoCapture(0)
video_capture.set(3, 340)
video_capture.set(4, 480)


while(True):

    
    ret,frame = video_capture.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    cv2.imshow('frame',hsv)
    #cv2.waitKey(1)
    
    lower = np.array(np.matrix([[30,100,100],[80,100,100],[0,39,64],[110,50,50]]))
    upper = np.array(np.matrix([[70,255,255],[105,255,255],[20,255,255],[130,255,255]]))
    

    mask_0 = cv2.inRange(hsv,lower[0], upper[0]) # creation du mask vert hsv
    

    
    mask = cv2.inRange(hsv,lower[3], upper[3])

    res = cv2.bitwise_and(frame,frame, mask=mask) # Application du mask sur la frame pour segmenter 
        
    gray_image = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)  # conversion de l image en niveau de gris
    ret,thresh = cv2.threshold(gray_image,127,255,0)  # binarisation

    M = cv2.moments(thresh)  # detecter la ligne
        
        
    cX = int(M["m10"] / M["m00"])  #coordonnees du centre en x
    cY = int(M["m01"] / M["m00"])  #coordonnees du centre en y
    print(cX)
    print(cY)
    cv2.circle(res, (cX, cY), 5, (255, 255, 255), -1)
    cv2.putText(res, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        

    # affichage de l image 
        
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 35: 
        break



cv2.destroyAllWindows()