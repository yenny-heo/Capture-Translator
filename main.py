import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

from PIL import ImageGrab
x1 = 0
y1 = 0
x2 = 0
y2 = 0

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

        self.setWindowTitle('Yenny Application')
        self.move(300, 300)
        self.resize(400, 200)
        self.show()

    def capture(self):
        self.setWindowOpacity(0)
        self.move(0, 0)
        self.resize(1920, 1080)
        self.fillColor = QtGui.QColor(30, 30, 30, 0)
        self.setMouseTracking(True)

    def mousePressEvent(self, e):  # e ; QMouseEvent
        global x1
        global y1
        x1 = e.globalX()
        y1 = e.globalY()
        print(e.globalX(), e.globalY())

    def mouseReleaseEvent(self, e): # e ; QMouseEvent
        global x2
        global y2
        x2 = e.globalX()
        y2 = e.globalY()
        print(e.globalX(), e.globalY())
        imageGrab(x1, y1, x2, y2)
        self.setWindowOpacity(100)
        self.move(300, 300)
        self.resize(400, 200)
        self.setMouseTracking(False)


def imageGrab(x1, y1, x2, y2):
    img = ImageGrab.grab((x1, y1, x2, y2))
    img.save('./test.png')
    img.show()

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())