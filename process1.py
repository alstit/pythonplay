
import sys 
# Takes first name and last name via command  
# line arguments and then display them 

 
  
import numpy as np
from PIL import Image
import cv2
import pyvjoy
import win32gui, win32ui, win32con, win32api
import sys


def grab_screen(region=None):

    hwin = win32gui.GetDesktopWindow()

    if region:
            left,top,x2,y2 = region
            width = x2 - left + 1
            height = y2 - top + 1
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    
    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height,width,4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())
    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)





def main() :
    filepath = sys.argv[1]
    #print 'Number of arguments:', len(sys.argv), 'arguments.'
    #print 'Argument List:', str(sys.argv)
    # value = 80
    j = pyvjoy.VJoyDevice(1)
    inv_direction=0
#while (True) :
    screen = cv2.imread(filepath)
    #screen = np.array(ImageGrab.grab(bbox=(0,40,800,600)))
    #screen = grab_screen(region =(0,40,800,600))
    #cv2.imshow('window', screen)
    # From BGR to HSV color space
    processed_img = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)
    # HSV range definition values are from (0,0,0) to (255,255,255)
    lower = np.array([0,10,50])
    upper = np.array([255,75,150])
    # image crop
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
        cx = 400
        cy= 0
    
    
    # draw a line from ground of screen to centroid of the contour
    cv2.line(mask,(400,600),(cx,cy),(0,80,255),5)
    
    
    inv_direction = -(400-cx)/(600-cy)
    inv_direction = int((np.uint16(inv_direction*3278))/2)
    j.set_axis(pyvjoy.HID_USAGE_X, inv_direction)
    
    #cv2.imshow('window', mask)
    cv2.imwrite("./upload/",mask)
    
    # if cv2.waitKey(10) & 0xFF == ord('u'):
        # print (value)
        # value+=1
        
    # if cv2.waitKey(10) & 0xFF == ord('i'):
        # value+=-1
        # print(value)
    
    if cv2.waitKey(10) & 0xFF == ord('e'):
        cv2.destroyAllWindows()
        break
	   
	   
if __name__ == "__main__":
    main()
    
    
    
    
    
