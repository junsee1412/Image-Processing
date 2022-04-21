import cv2
import numpy as np

class Process:
    def changeBrightness(self, img, value):
        hsv =cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h,s,v = cv2.split(hsv)
        lim = 255 - value
        v[v>lim] = 255
        v[v<=lim] += value
        final_hsv = cv2.merge((h,s,v))
        img = cv2.cvtColor(final_hsv,cv2.COLOR_HSV2BGR)
        return img
    
    def changeBlur(self, img, value):
        kernel_size = (value + 1, value + 1)
        img = cv2.blur(img, kernel_size)
        return img

    def changeGamma(self, img, value):
        value = value*0.1
        invGamma = 1.0 /value
        table = np.array([((i / 255.0) ** invGamma) * 255
            for i in np.arange(0, 256)]).astype("uint8")

        img = cv2.LUT(img, table)
        return img