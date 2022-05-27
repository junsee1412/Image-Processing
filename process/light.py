import cv2
import numpy as np

class Light:
    def change_Color(self, img, red, green, blue, alpha):
        img = cv2.convertScaleAbs(img, alpha=alpha*0.01)
        b, g, r = cv2.split(img)

        for r_value in r:
            cv2.add(r_value, red, r_value)
        for g_value in g:
            cv2.add(g_value, green, g_value)
        for b_value in b:
            cv2.add(b_value, blue, b_value)

        img = cv2.merge((b, g, r))
        return img

    def change_Gamma(self, img, value):
        value = value*0.02
        invGamma = 1.0 /value
        table = np.array([((i / 255.0) ** invGamma) * 255
            for i in np.arange(0, 256)]).astype("uint8")

        img = cv2.LUT(img, table)
        return img
    
    def change_Contrast(self, img, value):
        f = 131*(value + 127)/(127*(131-value))
        alpha_c = f
        gamma_c = 127*(1-f)
        img = cv2.addWeighted(img, alpha_c, img, 0, gamma_c)
        return img