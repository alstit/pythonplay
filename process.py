import sys 
import numpy as np
from PIL import Image
import cv2
import pyvjoy
import win32gui, win32ui, win32con, win32api
import sys
from datetime import datetime






def getdirection(screen,width=800):
    processed_img = cv2.cvtColor(screen, cv2.COLOR_RGB2HSV)
    
    # HSV range definition values are from (0,0,0) to (255,255,255)
    lower = np.array([50,10,50])
    upper = np.array([150,70,130])
    
    # image threshold
    mask = cv2.inRange(processed_img,lower,upper)
    mask = cv2.GaussianBlur(mask,(3,3),0)
    
    # find contours
    contours,hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(mask, contours, -1, (80,255,80), 1)

    # searching the biggest contour
    c=max(contours,key=cv2.contourArea)
    
    # approximate the contour with a polygonal shape
    epsilon = 0.01*cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c,epsilon,True)
    
    cv2.drawContours(mask,[approx],-1,(100,255,100),3)
    
    
    
    
    
    
    # find centroid
    M = cv2.moments(approx)
    if(M["m00"]!=0):
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
    else :
        cx = width/2
        cy= 0
    return mask, cx,cy





def main() :
    lines = sys.stdin.buffer.read();

    image=np.frombuffer(lines, dtype="uint8")
    
    
    screen = cv2.imdecode(image,cv2.IMREAD_UNCHANGED)
    
    
    
    
    height, width, channels = screen.shape
    
    mask,cx,cy = getdirection(screen,width)
    
    inv_direction = (cx-width/2)/(cy-height)
    
    
    
    cv2.imwrite("./uploads/"+datetime.now().strftime("%m%d%Y%H%M%S%f")+".png",mask)

    
    print(inv_direction)

    
if __name__ == "__main__":
    main()
    
    
    
    
    

    
    
