from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QImage, QPixmap, QMouseEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGraphicsPixmapItem, QGraphicsScene, QFileDialog, qApp
from gui.maingui import Ui_MainWindow
from process.smoothing import Smoothing
from process.adjust import Adjust
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
        self.mwg.actionZoom_In.triggered.connect(self.on_zoom_in)
        self.mwg.actionZoom_Out.triggered.connect(self.on_zoom_out)

        # Tab
        # tab 1
        self.mwg.sliderBrightness.valueChanged['int'].connect(self.alpha_value)
        self.mwg.sliderRed.valueChanged['int'].connect(self.red_value)
        self.mwg.sliderGreen.valueChanged['int'].connect(self.green_value)
        self.mwg.sliderBlue.valueChanged['int'].connect(self.blue_value)
        self.mwg.sliderGamma.valueChanged['int'].connect(self.gamma_value)

        # tab 2
        self.mwg.sliderBlur.valueChanged['int'].connect(self.blur_value)
        self.mwg.sliderGaussian.valueChanged['int'].connect(self.gauss_value)
        self.mwg.slideMedian.valueChanged['int'].connect(self.medi_value)

        # tab 3
        self.mwg.radio_None.clicked.connect(self.radio_state)
        self.mwg.radio_Bilateral.clicked.connect(self.radio_state)
        self.mwg.radio_Blackwhite.clicked.connect(self.radio_state)
        self.mwg.radio_Box.clicked.connect(self.radio_state)
        self.mwg.radio_Emboss.clicked.connect(self.radio_state)
        self.mwg.radio_Directional_1.clicked.connect(self.radio_state)
        self.mwg.radio_Directional_2.clicked.connect(self.radio_state)
        self.mwg.radio_Directional_3.clicked.connect(self.radio_state)
        self.mwg.radio_Median_threshold.clicked.connect(self.radio_state)
        self.mwg.radio_Negative.clicked.connect(self.radio_state)
        self.mwg.radio_Sepia.clicked.connect(self.radio_state)

        # Tools
        self.mwg.actionRotateLeft.triggered.connect(lambda:self.rotate(cv2.ROTATE_90_COUNTERCLOCKWISE))
        self.mwg.actionRotateRight.triggered.connect(lambda:self.rotate(cv2.ROTATE_90_CLOCKWISE))
        self.mwg.actionCursor.triggered.connect(lambda:self.pushAction(self.mwg.actionCursor))
        self.mwg.actionPen.triggered.connect(lambda:self.pushAction(self.mwg.actionPen))
        self.mwg.actionEraser.triggered.connect(lambda:self.pushAction(self.mwg.actionEraser))
        self.mwg.actionMove.triggered.connect(lambda:self.pushAction(self.mwg.actionMove))
        self.mwg.actionCrop.triggered.connect(lambda:self.pushAction(self.mwg.actionCrop))
        self.mwg.actionBrush.triggered.connect(lambda:self.pushAction(self.mwg.actionBrush))
        self.mwg.actionFillColor.triggered.connect(lambda:self.pushAction(self.mwg.actionFillColor))
        self.mwg.actionPicker.triggered.connect(lambda:self.pushAction(self.mwg.actionPicker))
        self.mwg.actionCursor.setChecked(True)

        self.mwg.graphicsView.viewport().installEventFilter(self)
        self.mwg.scrollArea.setMouseTracking(True)

        self.mwg.actionQuit.triggered.connect(qApp.quit)
        
        self.smoothing = Smoothing()
        self.adjust = Adjust()
        self.filter = Filter()
        self.tools = Tools()
        self.path = None
        self.img = None
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

        if (event.type() == QEvent.MouseMove):
            print(f"x: {event.x()}, y: {event.y()}")

        return super().eventFilter(source, event)
    
    def pushAction(self, action):
        print(action.text())
        for child in self.mwg.tools.actions():
            if not child.isSeparator():
                # if child != action:
                child.setChecked(False)
        action.toggle()

    def reset(self):
        self.alpha_value_now = 100
        self.red_value_now = 0
        self.green_value_now = 0
        self.blue_value_now = 0
        self.gamma_value_now = 50
        self.blur_value_now = 0
        self.gauss_value_now = 1
        self.medi_value_now = 1
        self.mwg.radio_None.setChecked(True)
        self.mwg.sliderBrightness.setValue(self.alpha_value_now)
        self.mwg.sliderGamma.setValue(self.gamma_value_now)
        self.mwg.sliderBlur.setValue(self.blur_value_now)
        self.mwg.sliderGaussian.setValue(self.gauss_value_now)
        self.mwg.slideMedian.setValue(self.medi_value_now)
        self.mwg.tabWidget.setHidden(True)

    def loadImage(self):
        path = QFileDialog.getOpenFileName(self, "Open Image", self.directory, filter="Image (*.*)")[0]
        if (path):
            self.path = path
            self.reset()
            self.image = cv2.imread(self.path)
            self.setPhoto(self.image)
            name = os.path.basename(self.path)
            self.mwg.statusbar.showMessage(name)
            self.mwg.tabWidget.setHidden(False)

    def setPhoto(self, image):
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)

        item = QGraphicsPixmapItem(pixmap)
        scene = QGraphicsScene(self)
        scene.addItem(item)
        self.mwg.graphicsView.setScene(scene)
    
    def alpha_value(self, value):
        if (self.path):
            self.alpha_value_now = value
            self.update()
    
    def red_value(self, value):
        if (self.path):
            self.red_value_now = value
            self.update()
    
    def green_value(self, value):
        if (self.path):
            self.green_value_now = value
            self.update()
    
    def blue_value(self, value):
        if (self.path):
            self.blue_value_now = value
            self.update()
    
    def gamma_value(self, value):
        if (self.path):
            self.gamma_value_now = value
            self.update()
    
    def blur_value(self, value):
        if (self.path):
            self.blur_value_now = value
            self.update()

    def gauss_value(self, value):
        if (self.path):
            self.gauss_value_now = value
            self.update()

    def medi_value(self, value):
        if (self.path):
            self.medi_value_now = value
            self.update()

    def radio_state(self):
        if (self.path):
            self.update()
    
    def filter_select(self, img):
        if (self.mwg.radio_Bilateral.isChecked()):
            img = self.filter.Bilateral(img)
        elif (self.mwg.radio_Box.isChecked()):
            img = self.filter.Box(img)
        elif (self.mwg.radio_Blackwhite.isChecked()):
            img = self.filter.Black_white(img)
        elif (self.mwg.radio_Directional_1.isChecked()):
            img = self.filter.Directional_1(img)
        elif (self.mwg.radio_Directional_2.isChecked()):
            img = self.filter.Directional_2(img)
        elif (self.mwg.radio_Directional_3.isChecked()):
            img = self.filter.Directional_3(img)
        elif (self.mwg.radio_Median_threshold.isChecked()):
            img = self.filter.Median_threshold(img)
        elif (self.mwg.radio_Negative.isChecked()):
            img = self.filter.Negative(img)
        elif (self.mwg.radio_Sepia.isChecked()):
            img = self.filter.Sepia(img)

        return img
    
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
    
    def update(self):
        img = self.adjust.change_Color(self.image, self.red_value_now, self.green_value_now, self.blue_value_now, self.alpha_value_now)
        img = self.adjust.change_Gamma(img, self.gamma_value_now)
        img = self.smoothing.change_Blur(img, self.blur_value_now)
        img = self.smoothing.change_Median(img, self.medi_value_now)
        img = self.smoothing.change_Gaussian(img, self.gauss_value_now)
        img = self.filter_select(img)
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