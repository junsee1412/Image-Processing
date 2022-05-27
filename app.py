from PyQt5.QtCore import QEvent, Qt, QPoint
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGraphicsPixmapItem, QGraphicsScene, QFileDialog, qApp
from gui.maingui import Ui_MainWindow
from process.smoothing import Smoothing
from process.light import Light
from process.filter import Filter
from process.tools import Tools
import sys, os, cv2

class MainMeow(QWidget):

    def __init__(self):
        super().__init__()
        self.main_win = QMainWindow()
        self.mwg = Ui_MainWindow()
        self.mwg.setupUi(self.main_win)

        self.mwg.actionOpen.triggered.connect(self.loadImage)
        self.mwg.actionSave.triggered.connect(self.savePhoto)
        self.mwg.actionSave_as.triggered.connect(self.saveasPhoto)
        self.mwg.actionZoom_In.triggered.connect(self.on_zoom_in)
        self.mwg.actionZoom_Out.triggered.connect(self.on_zoom_out)

        # Feature
        # tab 1
        self.mwg.sliderBrightness.valueChanged['int'].connect(self.alpha_value)
        self.mwg.sliderRed.valueChanged['int'].connect(self.red_value)
        self.mwg.sliderGreen.valueChanged['int'].connect(self.green_value)
        self.mwg.sliderBlue.valueChanged['int'].connect(self.blue_value)
        self.mwg.sliderGamma.valueChanged['int'].connect(self.gamma_value)
        self.mwg.sliderContrast.valueChanged['int'].connect(self.contrast_value)

        # tab 2
        self.mwg.sliderBlur.valueChanged['int'].connect(self.blur_value)
        self.mwg.sliderGaussian.valueChanged['int'].connect(self.gauss_value)
        self.mwg.sliderBox.valueChanged['int'].connect(self.box_value)
        self.mwg.slideMedian.valueChanged['int'].connect(self.medi_value)
        self.mwg.check_Threshold.clicked.connect(lambda:self.medi_value(self.mwg.slideMedian.value()))

        # tab 3
        self.mwg.radio_None.clicked.connect(self.radio_state)
        self.mwg.radio_Bilateral.clicked.connect(self.radio_state)
        self.mwg.radio_Blackwhite.clicked.connect(self.radio_state)
        self.mwg.radio_Emboss.clicked.connect(self.radio_state)
        self.mwg.radio_Directional_1.clicked.connect(self.radio_state)
        self.mwg.radio_Directional_2.clicked.connect(self.radio_state)
        self.mwg.radio_Directional_3.clicked.connect(self.radio_state)
        self.mwg.radio_Negative.clicked.connect(self.radio_state)
        self.mwg.radio_Sepia.clicked.connect(self.radio_state)

        # Queue
        self.mwg.listWidget.clicked.connect(self.selectItemQueue)
        self.mwg.push_Original.clicked.connect(lambda:self.setPhoto(self.origin))
        self.mwg.push_Changed.clicked.connect(lambda:self.setPhoto(self.img))
        self.mwg.push_Remove.clicked.connect(self.removeItemQueue)
        self.mwg.push_Clear.clicked.connect(self.clearQueue)

        # Tools
        self.mwg.actionRotateLeft.triggered.connect(lambda:self.rotate(cv2.ROTATE_90_COUNTERCLOCKWISE))
        self.mwg.actionRotateRight.triggered.connect(lambda:self.rotate(cv2.ROTATE_90_CLOCKWISE))
        self.mwg.actionFlipH.triggered.connect(lambda:self.flip(0))
        self.mwg.actionFlipV.triggered.connect(lambda:self.flip(1))
        self.mwg.actionRemoveBg.triggered.connect(self.remove_background)

        self.mwg.graphicsView.viewport().installEventFilter(self)
        self.mwg.scrollArea.setMouseTracking(True)

        self.mwg.actionQuit.triggered.connect(qApp.quit)
        
        self.smoothing = Smoothing()
        self.light = Light()
        self.filter = Filter()
        self.tools = Tools()
        self.path = None
        self.image = None
        self.img = None
        self.origin = None
        self.scene = None
        self.brushSize = 1
        self.brushColor = Qt.black
        self.lastPoint = QPoint()
        self.reset()
        self.queueProcess = []
        self.directory = os.path.expanduser("~")
        
    def eventFilter(self, source, event):
        if (
            event.type() == QEvent.Wheel and
            event.modifiers() == Qt.ControlModifier):
                if event.angleDelta().y() > 0:
                    scale = 1.25
                else:
                    scale = 0.8
                self.mwg.graphicsView.scale(scale, scale)

                return True

        return super().eventFilter(source, event)

    def reset(self):
        self.alpha_value_now = 100
        self.red_value_now = 0
        self.green_value_now = 0
        self.blue_value_now = 0
        self.gamma_value_now = 50
        self.contrast_value_now = 0
        self.blur_value_now = 0
        self.box_value_now = 1
        self.gauss_value_now = 1
        self.medi_value_now = 1
        self.mwg.radio_None.setChecked(True)
        self.queueProcess = []
        self.select = None

        self.mwg.sliderBrightness.setValue(self.alpha_value_now)
        self.mwg.sliderRed.setValue(self.red_value_now)
        self.mwg.sliderGreen.setValue(self.green_value_now)
        self.mwg.sliderBlue.setValue(self.blue_value_now)
        self.mwg.sliderGamma.setValue(self.gamma_value_now)
        self.mwg.sliderContrast.setValue(self.contrast_value_now)

        self.mwg.sliderBlur.setValue(self.blur_value_now)
        self.mwg.sliderGaussian.setValue(self.gauss_value_now)
        self.mwg.sliderBox.setValue(self.box_value_now)
        self.mwg.slideMedian.setValue(self.medi_value_now)

        self.mwg.push_Remove.setDisabled(True)
        if (not self.path):
            self.mwg.toolBox.setHidden(True)
        else:
            self.image = cv2.imread(self.path)
            self.setPhoto(self.image)

    def loadImage(self):
        path = QFileDialog.getOpenFileName(self, "Open Image", self.directory, filter="Image (*.*)")[0]
        if (path):
            self.path = path
            self.reset()
            self.image = cv2.imread(self.path)
            self.origin = self.image
            self.setPhoto(self.image)
            name = os.path.basename(self.path)
            self.mwg.statusbar.showMessage(name)
            self.mwg.toolBox.setHidden(False)

    def setPhoto(self, image):
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)

        item = QGraphicsPixmapItem(pixmap)
        self.scene = QGraphicsScene(self)
        self.scene.addItem(item)
        self.mwg.graphicsView.setScene(self.scene)
    
    def alpha_value(self, value):
        if (self.path):
            self.alpha_value_now = value
            if not self.process_Color in self.queueProcess:
                self.queueProcess.append(self.process_Color)
            self.update()
    
    def red_value(self, value):
        if (self.path):
            self.red_value_now = value
            if not self.process_Color in self.queueProcess:
                self.queueProcess.append(self.process_Color)
            self.update()
    
    def green_value(self, value):
        if (self.path):
            self.green_value_now = value
            if not self.process_Color in self.queueProcess:
                self.queueProcess.append(self.process_Color)
            self.update()
    
    def blue_value(self, value):
        if (self.path):
            self.blue_value_now = value
            if not self.process_Color in self.queueProcess:
                self.queueProcess.append(self.process_Color)
            self.update()
    
    def gamma_value(self, value):
        if (self.path):
            self.gamma_value_now = value
            if not self.process_Gamma in self.queueProcess:
                self.queueProcess.append(self.process_Gamma)
            self.update()
    
    def contrast_value(self, value):
        if (self.path):
            self.contrast_value_now = value
            if not self.process_Contrast in self.queueProcess:
                self.queueProcess.append(self.process_Contrast)
            self.update()
    
    def blur_value(self, value):
        if (self.path):
            self.blur_value_now = value
            if not self.process_Blur in self.queueProcess:
                self.queueProcess.append(self.process_Blur)
            self.update()

    def gauss_value(self, value):
        if (self.path):
            self.gauss_value_now = value
            if not self.process_Gaussian in self.queueProcess:
                self.queueProcess.append(self.process_Gaussian)
            self.update()

    def box_value(self, value):
        if (self.path):
            self.box_value_now = value
            if not self.process_Box in self.queueProcess:
                self.queueProcess.append(self.process_Box)
            self.update()

    def medi_value(self, value):
        if (self.path):
            self.medi_value_now = value
            if not self.process_Median in self.queueProcess:
                self.queueProcess.append(self.process_Median)
            self.update()

    def radio_state(self):
        if (self.path):
            if not self.process_Filter in self.queueProcess:
                self.queueProcess.append(self.process_Filter)
            self.update()
    
    def remove_background(self):
        if (self.path):
            if not self.process_RemoveBG in self.queueProcess:
                self.queueProcess.append(self.process_RemoveBG)
            self.update()
    
    def process_Color(self, img):
        img = self.light.change_Color(self.image, self.red_value_now, self.green_value_now, self.blue_value_now, self.alpha_value_now)
        return img

    def process_Gamma(self, img):
        img = self.light.change_Gamma(img, self.gamma_value_now)
        return img

    def process_Contrast(self, img):
        img = self.light.change_Contrast(img, self.contrast_value_now)
        return img
    
    def process_Blur(self, img):
        img = self.smoothing.change_Blur(img, self.blur_value_now)
        return img
    
    def process_Median(self, img):
        img = self.smoothing.change_Median(img, self.medi_value_now, self.mwg.check_Threshold.isChecked())
        return img

    def process_Box(self, img):
        img = self.smoothing.change_Box(img, self.box_value_now)
        return img
    
    def process_Gaussian(self, img):
        img = self.smoothing.change_Gaussian(img, self.gauss_value_now)
        return img
    
    def process_Filter(self, img):
        if (self.mwg.radio_Bilateral.isChecked()):
            img = self.filter.Bilateral(img)
        elif (self.mwg.radio_Blackwhite.isChecked()):
            img = self.filter.Black_white(img)
        elif (self.mwg.radio_Directional_1.isChecked()):
            img = self.filter.Directional_1(img)
        elif (self.mwg.radio_Directional_2.isChecked()):
            img = self.filter.Directional_2(img)
        elif (self.mwg.radio_Directional_3.isChecked()):
            img = self.filter.Directional_3(img)
        elif (self.mwg.radio_Emboss.isChecked()):
            img = self.filter.Emboss(img)
        elif (self.mwg.radio_Negative.isChecked()):
            img = self.filter.Negative(img)
        elif (self.mwg.radio_Sepia.isChecked()):
            img = self.filter.Sepia(img)

        return img
    
    def process_RemoveBG(self, img):
        img = self.tools.bgremove(img)
        return img

    def removeItemQueue(self):
        try:
            del self.queueProcess[self.select]
        except:
            pass
        self.mwg.push_Remove.setDisabled(True)
        self.update()

    def clearQueue(self):
        self.reset()
        self.queueProcess.clear()
        self.update()

    def selectItemQueue(self):
        item = self.mwg.listWidget.currentRow()
        self.select = item
        self.mwg.push_Remove.setEnabled(True)
    
    def checkbox_state(self, btn):
        self.update()

    def on_zoom_in(self):
        if (self.path):
            scale = 1.25
            self.mwg.graphicsView.scale(scale, scale)

    def on_zoom_out(self):
        if (self.path):
            scale = 0.8
            self.mwg.graphicsView.scale(scale, scale)

    def rotate(self, angle):
        if (self.path):
            self.image = self.tools.rotate(self.image, angle)
            self.update()
    
    def flip(self, code):
        if (self.path):
            self.image = self.tools.flip(self.image, code)
            self.update()
    
    def update(self):
        img = self.image
        proc_list = self.mwg.listWidget
        proc_list.clear()
        for prs in self.queueProcess:
            img = prs(img)
            item = str(prs).split(" ")[2].split("_")[1]
            proc_list.addItem(item)

        self.setPhoto(img)
        self.img = img
    
    def savePhoto(self):
        if (self.path):
            cv2.imwrite(self.path,self.img)
            self.reset()

    def saveasPhoto(self):
        filename = QFileDialog.getSaveFileName(self, "Save Image", self.directory, filter=".jpg;;.png;;.tiff;;.bmp")
        if (filename[0]):
            self.path = ''.join(filename)
            cv2.imwrite(self.path,self.img)
            name = os.path.basename(self.path)
            self.mwg.statusbar.showMessage(name)
            self.reset()

    def show(self):
        self.main_win.show()

if __name__ == "__main__":
    app = QApplication([])

    form = MainMeow()
    form.show()

    sys.exit(app.exec_())