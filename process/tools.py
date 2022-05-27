import cv2
import numpy as np

class Tools:
    
    def rotate(self, img, angle):
        img = cv2.rotate(img, angle)
        return img

    def flip(self, img, code):
        img = cv2.flip(img, code)
        return img
    
    def bgremove(self, myimage):
        myimage_hsv = cv2.cvtColor(myimage, cv2.COLOR_BGR2HSV)
        
        s = myimage_hsv[:,:,1]
        s = np.where(s < 127, 0, 1)

        v = (myimage_hsv[:,:,2] + 127) % 255
        v = np.where(v > 127, 1, 0)

        foreground = np.where(s+v > 0, 1, 0).astype(np.uint8)

        background = np.where(foreground==0,255,0).astype(np.uint8)
        background = cv2.cvtColor(background, cv2.COLOR_GRAY2BGR)
        foreground=cv2.bitwise_and(myimage,myimage,mask=foreground)
        finalimage = background+foreground

        return finalimage