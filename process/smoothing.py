import cv2

class Smoothing:
    def change_Blur(self, img, value):
        kernel_size = (value + 1, value + 1)
        img = cv2.blur(img, kernel_size)
        return img
    

    def change_Box(self, img, value):
        kernel_size = (value, value)
        img = cv2.boxFilter(img, -1, kernel_size)
        return img

    def change_Gaussian(self, img, value):
        if (value % 2 == 1):
            value = value
        else:
            value = value + 1

        kernel_size = (value, value)
        img = cv2.GaussianBlur(img, kernel_size, cv2.BORDER_DEFAULT)
        return img

    def change_Median(self, img, value, ts):
        if (value % 2 == 1):
            value = value
        else:
            value = value + 1

        img = cv2.medianBlur(img, value)
        
        if (ts):
            grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            retval, threshold = cv2.threshold(grayscaled,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            img = threshold

        return img