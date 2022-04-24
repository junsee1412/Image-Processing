import cv2
import numpy as np

class Process:

    # Ánh sáng:
    def change_Brightness(self, img, value):
        hsv =cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h,s,v = cv2.split(hsv)
        lim = 255 - value
        v[v>lim] = 255
        v[v<=lim] += value
        final_hsv = cv2.merge((h,s,v))
        img = cv2.cvtColor(final_hsv,cv2.COLOR_HSV2BGR)
        return img

    def change_Gamma(self, img, value):
        value = value*0.02
        invGamma = 1.0 /value
        table = np.array([((i / 255.0) ** invGamma) * 255
            for i in np.arange(0, 256)]).astype("uint8")

        img = cv2.LUT(img, table)
        return img
    
    # Lọc Mịn
    def change_Blur(self, img, value):
        kernel_size = (value + 1, value + 1)
        img = cv2.blur(img, kernel_size)
        return img

    def change_Gaussian(self, img, value):
        if (value % 2 == 1):
            kernel_size = (value, value)
            img = cv2.GaussianBlur(img, kernel_size, cv2.BORDER_DEFAULT)
        return img

    def change_Median(self, img, value):
        if (value % 2 == 1):
            img = cv2.medianBlur(img, value)
        return img
    
    # filter
    def filter_Bilateral(self, img):
        img = cv2.bilateralFilter(img,9,75,75)
        return img

    def filter_Box(self, img):
        img = cv2.boxFilter(img, -1,(20,20))
        return img

    def filter_Median_threshold(self, img):
        grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.medianBlur(img,5)
        retval, threshold = cv2.threshold(grayscaled,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        return threshold
        
    def filter_directional_1(self, img):
        kernel = np.ones((3, 3), np.float32) / 9
        img = cv2.filter2D(img, -1, kernel)
        return img
        
    def filter_directional_2(self, img):
        kernel = np.ones((5, 5), np.float32) / 9
        img = cv2.filter2D(img, -1, kernel)
        return img

    def filter_directional_3(self, img):
        kernel = np.ones((7, 7), np.float32) / 9
        img = cv2.filter2D(img, -1, kernel)
        return img

    def filter_butter(self, img):
        img_float32 = np.float32(img)

        dft = cv2.dft(img_float32, flags=cv2.DFT_COMPLEX_OUTPUT)
        img = np.fft.fftshift(dft)

        img = 20 * np.log(cv2.magnitude(img[:, :, 0], img[:, :, 1]))
        return img

    # def notch_filter(self):

    def inv_filter(self, img):
        for i in range(0, 3):
            g = img[:, :, i]
            G = (np.fft.fft2(g))

            # h = cv2.imread(img, 0)
            h_padded = np.zeros(g.shape)
            h_padded[:img.shape[0], :img.shape[1]] = np.copy(img)
            H = (np.fft.fft2(h_padded))

            # normalize to [0,1]
            H_norm = H / abs(H.max())
            G_norm = G / abs(G.max())
            F_temp = G_norm / H_norm
            F_norm = F_temp / abs(F_temp.max())

            # rescale to original scale
            F_hat = F_norm * abs(G.max())

            # 3. apply Inverse Filter and compute IFFT
            img = np.fft.ifft2(F_hat)
            img[:, :, i] = abs(img)
        return img