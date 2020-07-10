import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

from PIL import ImageGrab

x1 = 0
y1 = 0
x2 = 0
y2 = 0
captureFlag = False
dragFlag = False

class MyApp(QWidget):

    # 생성자
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        btn = QPushButton('capture', self)
        btn.move(50,50)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(self.capture)

        self.setWindowTitle('Capture and Translation')
        self.resize(400, 200)
        self.move(0,0)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.show()

    def paintEvent(self, a0):
        painter = QtGui.QPainter(self)
        if captureFlag and dragFlag:
            painter.setPen(QPen(QColor(60, 60, 60), 3))
            painter.drawRect(QtCore.QRect(self.begin, self.end))
        else:
            painter.drawRect(0,0,0,0)

    def capture(self):
        global captureFlag
        captureFlag = True
        self.setWindowOpacity(0.2)
        self.move(0,0)
        self.resize(1920, 1080)
        self.setMouseTracking(True)

    def mousePressEvent(self, e):  # e ; QMouseEvent
        if captureFlag:
            global x1
            global y1
            global dragFlag
            x1 = e.globalX()
            y1 = e.globalY()
            print(e.globalX(), e.globalY())
            dragFlag = True
            self.begin = e.pos()
            self.end = e.pos()
            self.update()


    def mouseMoveEvent(self, e):
        if captureFlag and dragFlag:
            self.end = e.pos()
            self.update()

    def mouseReleaseEvent(self, e): # e ; QMouseEvent
        global captureFlag
        if captureFlag:
            global x2
            global y2
            global dragFlag
            x2 = e.globalX()
            y2 = e.globalY()
            print(e.globalX(), e.globalY())

            dragFlag = False
            self.end = e.pos()
            self.update()

            imageGrab(x1, y1, x2, y2)
            self.setWindowOpacity(1)
            self.resize(400, 200)
            self.setMouseTracking(False)
            captureFlag = False


def imageGrab(x1, y1, x2, y2):
    a1 = x1 * 3360 / 1680
    b1 = y1 * 2100 / 1050
    a2 = x2 * 3360 / 1680
    b2 = y2 * 2100 / 1050
    print(a1, b1, a2, b2)
    img = ImageGrab.grab(bbox=(a1, b1, a2, b2))
    img.show()

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())