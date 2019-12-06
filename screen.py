import numpy as np
from PIL import ImageGrab
import cv2
import time
#import pyautogui
import scipy.ndimage
from numpy import ones,vstack
from numpy.linalg import lstsq
import win32gui, win32ui, win32con, win32api
import pyvjoy
from simple_pid import PID
from collections import deque

import statistics as st
from directkeys import ReleaseKey,PressKey, W, A, S, D





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

def straight():
    ReleaseKey(A)
    ReleaseKey(D)
    PressKey(W)
    


def left(direction):
    PressKey(A)
    ReleaseKey(D)
    ReleaseKey(W)



def right(direction):
    PressKey(D)
    ReleaseKey(A)
    ReleaseKey(W)

def slow_ya_roll():
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
    
    
def processed_img(image) :
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return processed_img    
    
def turns(image):
    processed_img = image
    # convert to gray
    
    #processed_img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # edge detection
    
    #mask creation for road select only HSV color for the road
    # Range for lower red
    lower_red = np.array([50,10,50])
    upper_red = np.array([150,70,130])
    #mask1 = cv2.inRange(processed_img, lower_red, upper_red)   
    
    
    vertices = np.array([[0,400],[0,200],[800,200],[800,400]], np.int32)
    # mask = cv2.GaussianBlur(mask,(5,5),0)
    roi = np.zeros_like(image)
    cv2.fillPoly(roi ,[vertices], (255,255,255))
    roi = cv2.bitwise_and(image, roi)

    mask = cv2.inRange(roi,lower_red,upper_red)

    contours,hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(mask, contours, -1, (80,255,80), 1)
    # # # searching the biggest contour
    # try:
    c=max(contours,key=cv2.contourArea)
    # # # searching the best approximation of the contour
    # # # line
    # # # [vx,vy,x,y] = cv2.fitLine(c,cv2.DIST_L2,0,0.01,0.01)
     # # # mask = cv2.line(mask,(512,768),(x,y),(80,255,80),3)
        # print(cv2.contourArea(c))
        # if(cv2.contourArea(c)<40000 and cv2.contourArea(c)>10000):
        # # # polygone
        # #if(True):
            # print(cv2.contourArea(c))
    epsilon = 0.002*cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c,epsilon,True)
    cv2.drawContours(mask,[approx],-1,(100,255,100),3)

        
        
        # # # find direction
        # # # direction = scipy.ndimage.measurements.center_of_mass(approx)
        # # # calcul du centre de mass du plus gros contour
        
    M = cv2.moments(approx)
        # # print(M)
    if(M["m00"]!=0):
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv2.line(mask,(400,400),(cx,cy),(100,80,255),5)
    else :
        cx = 400
        cy= 0
        
 

    return mask ,cx,cy





def road(image):
    processed_img = image
    # convert to gray
    blank_image = np.zeros((800,600,3), np.uint8)
    #processed_img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # edge detection
    
    #mask creation for road select only HSV color for the road
    # Range for paved
    lower_red = np.array([50,10,50])
    upper_red = np.array([150,70,130])
    
    #Range for greece
    #lower_red = np.array([0,100,0]7
    #upper_red = np.array([140,255,255])
    #mask1 = cv2.inRange(processed_img, lower_red, upper_red)   
    mask = cv2.inRange(processed_img,lower_red,upper_red)
    mask = cv2.GaussianBlur(mask,(5,5),0)
    #inv_mask=cv2.bitwise_not(mask)
    
    image=cv2.bitwise_and(image,image,mask=mask)
    #mask = cv2.Canny(mask,100,200)
    
    
    # find contour
    contours,hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, contours, -1, (80,255,80), 1)
    
    
    # #searching the biggest contour
    try :
        c=max(contours,key=cv2.contourArea)
    
    except: 
        print("no contour")
    
    
    
    
    
    
    
    # #searching the best approximation of the contour
    # #linedd
    # #[vx,vy,x,y] = cv2.fitLine(c,cv2.DISTqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq_L2,0,0.01,0.01)
     # #mask = cv2.line(mask,(512,768),(x,y),(80,255,80),3)
   
    # #polygone
    # #print(c)
    epsilon = 0.01*cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c,epsilon,True)
    #hull approx
    #approx = cv2.convexHull(c)
    cv2.drawContours(image,[approx],-1,(100,255,100),3)
    #find directionq
    #direction = scipy.ndimage.measurements.center_of_mass(approx)
    # #calcul du centre de mass du plus gros contour
    M = cv2.moments(approx)
    #print(M)
    if(M["m00"]!=0):
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        
    else :
        cx = 400
        cy= 0
    
    


 


    return image , cx, cy
    
    
def draw_lines(img,lines):
    a=0
    i=0
    for line in lines:
        coords = line[0]
        cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255,255,255], 3)
        if(abs(coords[2]-coords[0])>0.01):
            a+=(coords[3]-coords[1])/(coords[2]-coords[0])
            i+=1
    a=a/i
    return A

def drive(direction,j):
    inv_direction = direction
    print(direction)
    print((inv_direction)*16384+16384)
    #if(inv_direction>=0):
    inv_direction = int((inv_direction)*16384+16384)
    # if(inv_direction<0):
        # inv_direction = int(np.uint16((-inv_direction)*3278))    
    print(inv_direction)
    #print(direction)
    #print(inv_direction)
    #print(hex(inv_direction))
    j.set_axis(pyvjoy.HID_USAGE_X, inv_direction) 
    
    # if inv_direction > 1 :
        # #right(abs(inv_direction))
        # #j.set_button(1,1)
        # j.set_axis(pyvjoy.HID_USAGE_X, 0x8000)
        # #j.update()
        # print("right")
    # elif inv_direction < -1:
        # #left(abs(inv_direction))
        # j.set_axis(pyvjoy.HID_USAGE_X, 0x1)
        # #j.update
        # #j.set_button(1,0)
        # print("left")
    # else :
        # straight()
        # print("straight()")


def main():
    last_time = time.time()
    j = pyvjoy.VJoyDevice(1)
    pid = PID(0.1, 0, 0, setpoint=0)
    pid.output_limits = (-3,3)
    direction_mean = deque()
    cx_mean=deque()
    cy_mean=deque()
    while True:
        
        if(len(direction_mean)>3):
             direction_mean.popleft()
            # cx_mean.popleft()
            # cy_mean.popleft()
       # screen =  np.array(ImageGrab.grab(bbox=(0,40,800,600)))
        screen = grab_screen(region =(0,40,800,600))
        last_time = time.time()
        hsv = processed_img(screen)
        new_screen,cx,cy = road(hsv)
        virage,turnx,turny=turns(hsv)
        #new_screen,cx,cy = road(hsv)
        
        #cv2.imshow('window2',hsv)
        #cx_mean.append(cx)
        #cy_mean.append(cy)
        #cx=st.mean(cx_mean)
        #cy=st.mean(cy_mean)
        
        
        turn = (turnx-400)/(turny-400)
        
        if (abs(turn)> 5 ):
            print("turn ahead")
        
        
        
        direction = (cx-400)/(cy-800)
        cv2.line(new_screen,(400,600),(int(cx),int(cy)),(170,80,255),5)
        direction_mean.append(direction)
        direction=st.mean(direction_mean)
        #direction=pid(direction)

        print(direction)
        drive(direction,j)
        cv2.imshow('window', new_screen)
        cv2.imshow('virage',virage)
        

        #cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('e'):
            cv2.destroyAllWindows()
            break
            
            
            
            
            
            
if __name__ == "__main__":
    main();