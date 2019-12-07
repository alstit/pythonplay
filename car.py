
import sys 

import requests
from io import BytesIO
 
import numpy as np
from PIL import ImageGrab
import cv2
import pyvjoy
import win32gui, win32ui, win32con, win32api
import sys
from datetime  import datetime

def drive(direction,j):
    inv_direction = direction
    inv_direction = int((inv_direction)*16384+16384)
   
    print(inv_direction)

    j.set_axis(pyvjoy.HID_USAGE_X, inv_direction)



def main() :
    j = pyvjoy.VJoyDevice(1)


    while(True):
        screen = ImageGrab.grab(bbox=(0,40,800,600))
        stream = BytesIO()

        screen.save(stream,format = "PNG")

        files = {'myFile': stream.getvalue()}

        r= requests.post("http://localhost:3000/uploadfile",files=files)
        #print(type(r.content.decode('utf-8')))
        #print(float(r.content.decode('utf-8')))
        #print(r.content.decode('utf-8'))
        drive(float(r.content.decode('utf-8')),j)
    
if __name__ == "__main__":
    main()
    
    
    
    
    
