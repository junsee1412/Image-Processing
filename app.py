from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGraphicsPixmapItem, QGraphicsScene, QFileDialog, qApp
from gui.maingui import Ui_MainWindow
from process import Process
import sys, os, cv2

class MainMeow(QWidget):

    def __init__(self):
        super().__init__()
        self.main_win = QMainWindow()
        self.mwg = Ui_MainWindow()
        self.mwg.setupUi(self.main_win)

        self.mwg.actionOpen.triggered.connect(self.loadImage)
        self.mwg.actionSave.triggered.connect(self.savePhoto)
        self.mwg.horizontalSlider.valueChanged['int'].connect(self.brightness_value)
        self.mwg.horizontalSlider_2.valueChanged['int'].connect(self.gamma_value)
        self.mwg.horizontalSlider_3.valueChanged['int'].connect(self.blur_value)
        self.mwg.actionZoom_In.triggered.connect(self.on_zoom_in)
        self.mwg.actionZoom_Out.triggered.connect(self.on_zoom_out)

        self.mwg.graphicsView.viewport().installEventFilter(self)

        self.mwg.actionQuit.triggered.connect(qApp.quit)
        
        self.process = Process()
        self.path = None
        self.tmp = None
        self.reset()
        self.directory = os.path.expanduser("~")
    
    def eventFilter(self, source, event):
        if (
            # source == self.mwg.graphicsView.viewport() and 
            event.type() == QEvent.Wheel and
            event.modifiers() == Qt.ControlModifier):
                if event.angleDelta().y() > 0:
                    scale = 1.25
                else:
                    scale = 0.8
                self.mwg.graphicsView.scale(scale, scale)

                return True
        # elif (event.type() == QEvent.GraphicsSceneMousePress):
        #     pass
            # ...
        return super().eventFilter(source, event)
    
    def reset(self):
        self.brightness_value_now = 0
        self.blur_value_now = 0
        self.gamma_value_now = 10
        self.mwg.horizontalSlider.setValue(self.brightness_value_now)
        self.mwg.horizontalSlider_2.setValue(self.gamma_value_now)
        self.mwg.horizontalSlider_3.setValue(self.blur_value_now)

    def loadImage(self):
        path = QFileDialog.getOpenFileName(self, "Open Image", self.directory, filter="Image (*.*)")[0]
        if (path):
            self.path = path
            self.reset()
            self.image = cv2.imread(self.path)
            self.setPhoto(self.image)
            name = os.path.basename(self.path)
            self.mwg.statusbar.showMessage(name)

    def setPhoto(self, image):
        self.tmp = image
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
    
    def gamma_value(self, value):
        if (self.path):
            self.gamma_value_now = value
            self.update()

    def on_zoom_in(self):
        if (self.path):
            scale = 1.25
            self.mwg.graphicsView.scale(scale, scale)

    def on_zoom_out(self):
        if (self.path):
            scale = 0.8
            self.mwg.graphicsView.scale(scale, scale)
    
    def update(self):
        img = self.process.changeBrightness(self.image, self.brightness_value_now)
        img = self.process.changeGamma(img, self.gamma_value_now)
        img = self.process.changeBlur(img, self.blur_value_now)
        self.setPhoto(img)

    def savePhoto(self):
        filename = QFileDialog.getSaveFileName(self, "Save Image", self.directory, filter=".jpg;;.png;;.tiff;;.bmp")
        if (filename[0]):
            self.path = ''.join(filename)
            cv2.imwrite(self.path,self.tmp)
            name = os.path.basename(self.path)
            self.mwg.statusbar.showMessage(name)

    def show(self):
        self.main_win.show()

if __name__ == "__main__":
    app = QApplication([])

    form = MainMeow()
    form.show()

    sys.exit(app.exec_())