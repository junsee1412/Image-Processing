import cv2
import numpy as np

class Filter:
    def kernel_generator(self, size):
        kernel = np.zeros((size, size), dtype=np.int8)
        for i in range(size):
            for j in range(size):
                if i < j:
                    kernel[i][j] = -1
                elif i > j:
                    kernel[i][j] = 1
        return kernel

    def Bilateral(self, img):
        img = cv2.bilateralFilter(img,9,75,75)
        return img

    def Black_white(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
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
        size = 5 
        s = 2
        height, width = img.shape[:2]
        y = np.ones((height, width), np.uint8) * 128
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        kernel = self.kernel_generator(size)
        kernel = np.rot90(kernel, s)
        res = cv2.add(cv2.filter2D(gray, -1, kernel), y)

        return res
    
    def Negative(self, img):
        img = cv2.bitwise_not(img)
        return img

    def Sepia(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # converting to RGB as sepia matrix is for RGB
        img = np.array(img, dtype=np.float64)
        img = cv2.transform(img, np.matrix([[0.393, 0.769, 0.189],
                                            [0.349, 0.686, 0.168],
                                            [0.272, 0.534, 0.131]]))
        img[np.where(img > 255)] = 255 # clipping values greater than 255 to 255
        img = np.array(img, dtype=np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return img