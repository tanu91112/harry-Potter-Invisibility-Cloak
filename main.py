#Importation
import cv2
import numpy as np
import time

fourCC = cv2. VideoWriter_fourcc(*'XVID')
#this is used to capture video in openCV
#fourCC is a 4-byte video code, used to specify the video code
#for Windows, the video code is "*'XVID'" and for Mac, it is "*'MJPG'"

out = cv2.VideoWriter('output.avi', fourCC,  20 ,(200,200))
#(fileName, fourCCvariable, framePerSec, frameSize)

cap = cv2.VideoCapture(0) #you can use 0 or 1 to capture the video

time.sleep(3)

#variables
count = 0
background = 0

#While this forloop runs,capture the background
for i in range(60): #capturing the background 60 times. 
    
    returnV, background = cap.read()
    #returnV is a boolean valuse which returns True if captured properly
    #background is the captured background in an array of pixels
    
background = np.flip(background , axis=1)
#flipping the background to avoid mirror image

while(cap.isOpened()): #While your camera is opened, this will run
    returnV, img = cap.read() #returnV is true or false
    if not(returnV): #if at any point , return becomes false , break the loop
        break
    count += 1 #keeping count of the number of times this run (no use1)
    img = np.flip(img, axis=1) #flipping the current video
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #converting your image to hsv
    lower_red = np.array([0,120,50]) #saturation  is 120-255, value is 50-200.
    upper_red = np.array([10, 255,255]) #https:tinyurl.com/hsvColors
    mask1 = cv2.inRange(hsv,lower_red, upper_red)
    
    lower_red = np.array([170,120,50]) #saturation  is 120-255, value is 50-200.
    upper_red = np.array([180, 255,255])
    mask2 = cv2.inRange(hsv,lower_red, upper_red)
    
    mask1 += mask2 #combining both masks
     
    mask1 = cv2.morphologyEx(mask1,cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
    
    '''MORPH_OPEN performs 2 operation: Erosion and Dilation
    Erotion removes extra whilte space (noise) from image , shrinking it
    Dilation is reverse of Erosion, wherein clean white space are added,
    making the images the same size'''
    
    
    #np.ones makes it so that every kernal is more smooth
    #np. uint8 makes it so that every kernal is within 0-255
    
    # https:/tinyurl.com/bitwiseOpenCV
    mask2 = cv2.bitwise_not(mask1)
    result1 = cv2.bitwise_and(img,img,mask=mask2)
    result2 = cv2.bitwise_and(background,background,mask=mask1)
    
    finalOutput = cv2.addWeighted(result1,1,result2,1,0)
    # equal dominanace of result1 and result 2 (0 is just neccessary for syntax)
    
    out.write(finalOutput)
    #shown in fourCC video writer as 'Magic'
    
    cv2.imshow('Magic!',finalOutput)
    
    #if you hold q for 1 second , the loop breaks
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
#when the loop breaks, everything stops
cap.release()
out.release()
cv2.destroyAllWindows()
    