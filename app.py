from PyQt5.QtCore import QEvent, QSize, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGraphicsPixmapItem, QGraphicsScene, QFileDialog, qApp
from matplotlib import scale
from gui.maingui import Ui_MainWindow
import sys, os, cv2, imutils
import numpy as np

class MainMeow(QWidget):

    def __init__(self):
        super().__init__()
        self.main_win = QMainWindow()
        self.mwg = Ui_MainWindow()
        self.mwg.setupUi(self.main_win)

        self.mwg.actionOpen.triggered.connect(self.loadImage)
        self.mwg.actionSave.triggered.connect(self.savePhoto)
        self.mwg.horizontalSlider.valueChanged['int'].connect(self.brightness_value)
        self.mwg.horizontalSlider_2.valueChanged['int'].connect(self.blur_value)
        self.mwg.actionZoom_In.triggered.connect(self.on_zoom_in)
        self.mwg.actionZoom_Out.triggered.connect(self.on_zoom_out)

        self.mwg.graphicsView.viewport().installEventFilter(self)

        self.mwg.actionQuit.triggered.connect(qApp.quit)
        
        self.path = None
        self.tmp = None
        self.brightness_value_now = 0
        self.blur_value_now = 0
        self.directory = os.path.expanduser("~")
    
    def eventFilter(self, source, event):
        if (source == self.mwg.graphicsView.viewport() and 
            event.type() == QEvent.Wheel and
            event.modifiers() == Qt.ControlModifier):
                if event.angleDelta().y() > 0:
                    scale = 1.25
                else:
                    scale = .8
                self.mwg.graphicsView.scale(scale, scale)
                # do not propagate the event to the scroll area scrollbars
                return True
        elif (event.type() == QEvent.GraphicsSceneMousePress):
            pass
            # ...
        return super().eventFilter(source,event)

    def loadImage(self):
        path = QFileDialog.getOpenFileName(self, "Open Image", self.directory, filter="Image (*.*)")[0]
        if (path):
            self.path = path
            self.scale = 1
            self.brightness_value_now = 0
            self.blur_value_now = 0
            self.image = cv2.imread(self.path)
            self.setPhoto(self.image)

    def setPhoto(self,image):
        self.tmp = image
        image = imutils.resize(image,width=640)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)

        item = QGraphicsPixmapItem(pixmap)
        scene = QGraphicsScene(self)
        scene.addItem(item)
        self.mwg.graphicsView.setScene(scene)
    
    def brightness_value(self, value):
        if (self.path):
            self.brightness_value_now = value
            self.update()
    
    def blur_value(self, value):
        if (self.path):
            self.blur_value_now = value
            self.update()
    
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

    def on_zoom_in(self):
        if (self.path):
            scale = 1.25
            self.mwg.graphicsView.scale(scale, scale)

    def on_zoom_out(self):
        if (self.path):
            scale = 0.8
            self.mwg.graphicsView.scale(scale, scale)
    
    def update(self):
        img = self.changeBrightness(self.image, self.brightness_value_now)
        img = self.changeBlur(img, self.blur_value_now)
        self.setPhoto(img)

    def savePhoto(self):
        filename = QFileDialog.getSaveFileName(self, "Save Image", self.directory, filter=".jpg;;.png;;.tiff;;.bmp")
        if (filename[0]):
            self.path = ''.join(filename)
            cv2.imwrite(self.path,self.tmp)

    def show(self):
        self.main_win.show()


if __name__ == "__main__":
    app = QApplication([])

    form = MainMeow()
    form.show()

    sys.exit(app.exec_())