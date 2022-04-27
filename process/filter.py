import cv2
import numpy as np

class Filter:
    def Bilateral(self, img):
        img = cv2.bilateralFilter(img,9,75,75)
        return img

    def Black_white(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img

    def Box(self, img):
        img = cv2.boxFilter(img, -1,(20,20))
        return img
        
    def Directional_1(self, img):
        kernel = np.ones((2, 2), np.float32) / 9
        img = cv2.filter2D(img, -1, kernel)
        return img
        
    def Directional_2(self, img):
        kernel = np.ones((3, 3), np.float32) / 9
        img = cv2.filter2D(img, -1, kernel)
        return img

    def Directional_3(self, img):
        kernel = np.ones((4, 4), np.float32) / 9
        img = cv2.filter2D(img, -1, kernel)
        return img
    
    def Emboss(self, img):
        kernel = np.array([[0, -1, -1],
                           [1, 0, -1],
                           [1, 1, 0]])

        img = cv2.filter2D(img, -1, kernel)
        return img

    def Median_threshold(self, img):
        grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.medianBlur(img,5)
        retval, threshold = cv2.threshold(grayscaled,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        return threshold
    
    def Negative(self, img):
        img = cv2.bitwise_not(img)
        return img

    def Sepia(self, img):
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])

        img = cv2.filter2D(img, -1, kernel)
        return img