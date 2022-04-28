import cv2
class Tools:
    
    def rotate(self, img, angle):
        # rows, cols, steps = img.shape
        # M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
        # img = cv2.warpAffine(img, M, (cols, rows))
        img = cv2.rotate(img, angle)
        return img