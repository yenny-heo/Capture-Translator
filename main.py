import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMainWindow, QDesktopWidget, \
    QTextEdit, QComboBox, QHBoxLayout

from PIL import ImageGrab

import io
import os

from google.cloud import vision
from google.cloud.vision import types
from googletrans import Translator

x1 = 0
y1 = 0
x2 = 0
y2 = 0
captureFlag = False
dragFlag = False
convertedText = ""

client = vision.ImageAnnotatorClient.from_service_account_json("./myKey.json")

lan = {'af': 'afrikaans', 'am': 'amharic', 'ar': 'arabic', 'az': 'azerbaijani', 'be': 'belarusian', 'bg': 'bulgarian', 'bn': 'bengali', 'bs': 'bosnian', 'ca': 'catalan', 'ceb': 'cebuano', 'co': 'corsican', 'cs': 'czech', 'cy': 'welsh', 'da': 'danish', 'de': 'german', 'el': 'greek', 'en': 'english', 'eo': 'esperanto', 'es': 'spanish', 'et': 'estonian', 'eu': 'basque', 'fa': 'persian', 'fi': 'finnish', 'fil': 'Filipino', 'fr': 'french', 'fy': 'frisian', 'ga': 'irish', 'gd': 'scots gaelic', 'gl': 'galician', 'gu': 'gujarati', 'ha': 'hausa', 'haw': 'hawaiian', 'he': 'Hebrew', 'hi': 'hindi', 'hmn': 'hmong', 'hr': 'croatian', 'ht': 'haitian creole', 'hu': 'hungarian', 'hy': 'armenian', 'id': 'indonesian', 'ig': 'igbo', 'is': 'icelandic', 'it': 'italian', 'iw': 'hebrew', 'ja': 'japanese', 'jw': 'javanese', 'ka': 'georgian', 'kk': 'kazakh', 'km': 'khmer', 'kn': 'kannada', 'ko': 'korean', 'ku': 'kurdish (kurmanji)', 'ky': 'kyrgyz', 'la': 'latin', 'lb': 'luxembourgish', 'lo': 'lao', 'lt': 'lithuanian', 'lv': 'latvian', 'mg': 'malagasy', 'mi': 'maori', 'mk': 'macedonian', 'ml': 'malayalam', 'mn': 'mongolian', 'mr': 'marathi', 'ms': 'malay', 'mt': 'maltese', 'my': 'myanmar (burmese)', 'ne': 'nepali', 'nl': 'dutch', 'no': 'norwegian', 'ny': 'chichewa', 'pa': 'punjabi', 'pl': 'polish', 'ps': 'pashto', 'pt': 'portuguese', 'ro': 'romanian', 'ru': 'russian', 'sd': 'sindhi', 'si': 'sinhala', 'sk': 'slovak', 'sl': 'slovenian', 'sm': 'samoan', 'sn': 'shona', 'so': 'somali', 'sq': 'albanian', 'sr': 'serbian', 'st': 'sesotho', 'su': 'sundanese', 'sv': 'swedish', 'sw': 'swahili', 'ta': 'tamil', 'te': 'telugu', 'tg': 'tajik', 'th': 'thai', 'tl': 'filipino', 'tr': 'turkish', 'uk': 'ukrainian', 'ur': 'urdu', 'uz': 'uzbek', 'vi': 'vietnamese', 'xh': 'xhosa', 'yi': 'yiddish', 'yo': 'yoruba', 'zh-cn': 'chinese (simplified)', 'zh-tw': 'chinese (traditional)', 'zu': 'zulu'}
targetLan = 'ko'

class MyApp(QWidget):

    # 생성자
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.lb1 = QLabel('Target Language: ', self)
        self.lb1.setAlignment(Qt.AlignCenter)

        self.cb = QComboBox(self)
        for k, v in lan.items():
            self.cb.addItem(v)
        self.cb.setCurrentIndex((list(lan).index(targetLan)))

        self.cb.activated[str].connect(self.onActivated)

        self.btn = QPushButton('캡처하고 번역하기', self)
        self.btn.setFixedHeight(50)
        self.btn.resize(self.btn.sizeHint())
        self.btn.clicked.connect(self.capture)

        self.lb2 = QLabel('@made by yenny', self)
        self.lb2.setAlignment(Qt.AlignCenter)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.lb1)
        hbox.addWidget(self.cb)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addWidget(self.btn)
        vbox.addWidget(self.lb2)
        vbox.addStretch(1)

        self.setLayout(vbox)

        self.setWindowTitle('Capture Translator')
        self.resize(300, 150)
        self.move(0,0)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.show()

    def onActivated(self, text):
        global targetLan
        values = list(lan.values())
        idx = values.index(text)
        targetLan = list(lan)[idx]


    def capture(self):
        global captureFlag
        captureFlag = True

        self.lb1.setStyleSheet("color: rgba(255, 255, 255, 0);")
        self.cb.setStyleSheet("color: rgba(255, 255, 255, 0); background-color: rgba(255, 255, 255, 0);")
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
            global convertedText
            x2 = e.globalX()
            y2 = e.globalY()

            dragFlag = False
            self.end = e.pos()
            self.update()

            convertedText = imageGrab(x1, y1, x2, y2)
            self.dialog = ResultWindow(self)
            self.dialog.show()

            self.lb1.setStyleSheet("color: rgb(0, 0, 0);")
            self.cb.setStyleSheet("color: rgb(0, 0, 0);")
            self.btn.setStyleSheet("color: rgb(0, 0, 0);")
            self.lb2.setStyleSheet("color: rgb(0, 0, 0);")

            self.setWindowOpacity(1)
            self.resize(300, 150)
            self.setMouseTracking(False)
            captureFlag = False

class ResultWindow(QMainWindow):
    def __init__(self, parent):
        super(ResultWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.result = QTextEdit()
        self.result.setAcceptRichText(False)
        self.result.setText(convertedText)

        vbox = QVBoxLayout()
        vbox.addWidget(self.result)

        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(vbox)
        self.setWindowTitle('번역 결과')
        self.resize(400, 200)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

def imageGrab(x1, y1, x2, y2):
    a1 = x1 * 3360 / 1680
    b1 = y1 * 2100 / 1050
    a2 = x2 * 3360 / 1680
    b2 = y2 * 2100 / 1050
    img = ImageGrab.grab(bbox=(a1, b1, a2, b2))
    img.save("./test.png")
    return callGoogleVisionAPI()

def callGoogleVisionAPI():
    file_name = os.path.abspath("./test.png")
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    sentences = texts[0].description
    sentences = sentences.replace('\n', ' ')
    print(sentences)
    return callGoogleTrans(sentences)

def callGoogleTrans(sentences):
    translator = Translator()
    result = translator.translate(sentences, dest=targetLan)
    print(result.text)
    return result.text

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())