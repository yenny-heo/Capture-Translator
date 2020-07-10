import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout

from PIL import ImageGrab

import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

x1 = 0
y1 = 0
x2 = 0
y2 = 0
captureFlag = False
dragFlag = False

client = vision.ImageAnnotatorClient.from_service_account_json("./myKey.json")

class MyApp(QWidget):

    # 생성자
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.lb1 = QLabel('English -> Korean Translation', self)
        self.lb1.setAlignment(Qt.AlignCenter)

        self.btn = QPushButton('캡처하고 번역하기', self)
        self.btn.setFixedHeight(50)
        self.btn.resize(self.btn.sizeHint())
        self.btn.clicked.connect(self.capture)

        self.lb2 = QLabel('@made by yenny', self)
        self.lb2.setAlignment(Qt.AlignCenter)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.lb1)
        vbox.addWidget(self.btn)
        vbox.addWidget(self.lb2)
        vbox.addStretch(1)

        self.setLayout(vbox)

        self.setWindowTitle('Capture and Translation')
        self.resize(300, 150)
        self.move(0,0)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.show()

    def capture(self):
        global captureFlag
        captureFlag = True

        self.lb1.setStyleSheet("color: rgba(255, 255, 255, 0);")
        self.btn.setStyleSheet("color: rgba(255, 255, 255, 0); background-color: rgba(255, 255, 255, 0);")
        self.lb2.setStyleSheet("color: rgba(255, 255, 255, 0);")

        self.setWindowOpacity(0.25)
        self.move(0, 0)
        self.resize(1920, 1080)
        self.setMouseTracking(True)

    def paintEvent(self, a0):
        painter = QtGui.QPainter(self)
        if captureFlag and dragFlag:
            painter.setPen(QPen(Qt.red, 5))
            painter.drawRect(QtCore.QRect(self.begin, self.end))
        else:
            painter.drawRect(0,0,0,0)

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

            self.lb1.setStyleSheet("color: rgb(0, 0, 0);")
            self.btn.setStyleSheet("color: rgb(0, 0, 0);")
            self.lb2.setStyleSheet("color: rgb(0, 0, 0);")

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
    img.save("./test.png")
    img.show()

    file_name = os.path.abspath("./test.png")
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print(texts[0].description)

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())