
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





def main() :

    while(True):
        screen = ImageGrab.grab(bbox=(0,40,800,600))
        stream = BytesIO()

        screen.save(stream,format = "PNG")

        files = {'myFile': stream.getvalue()}

        r= requests.post("http://localhost:3000/uploadfile",files=files)
        print(r.content)

    
if __name__ == "__main__":
    main()
    
    
    
    
    
