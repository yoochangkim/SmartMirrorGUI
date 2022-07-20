import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from video import *
from tensorflow.keras import models
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

form_class = uic.loadUiType("layout/layout.ui")[0]

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pixmap = QtGui.QPixmap('layout/face.jpg')
        self.backgroundImg.setPixmap(self.pixmap)
        self.logo = QtGui.QPixmap('layout/logo.png')
        self.logoImg.setPixmap(self.logo)
        self.video = video(self,QSize(400,300), 1)
        self.camButton.setCheckable(True)
        self.camButton.clicked.connect(self.onoffCam)
        self.captureButton.setCheckable(True)
        self.captureButton.clicked.connect(self.captureCam)
        self.analysisButton.clicked.connect(self.fileOpen)
        self.modelButton.clicked.connect(self.modelLoad)

    def modelLoad(self):
        self.model = models.load_model("model/InceptionResnetV2_Model.h5")
        self.model.summary()
        #print(self.model.predict(self.fname))

    def fileOpen(self):
        filter = 'image(*.png *.jpg *.jpeg *.PNG) (*.png *.jpg *.jpeg *.PNG)'
        self.image_path = QFileDialog.getOpenFileNames(self, filter=filter)
        self.image_path = self.image_path[0][0]
        image = QPixmap()
        image.load(self.image_path)
        self.loadImg.setPixmap(image)
        #self.model = models.load_model("model/InceptionResnetV2_Model.h5")
        #print(self.model.predict(self.fname))
        #self.textEdit.clear()

    def recvImage(self, img):
        self.camView.setPixmap(QPixmap.fromImage(img))

    def closeEvent(self, e):
        self.video.stopCam()

    def captureCam(self, e):
        if self.camButton.isChecked():
            self.video.captureCam()
            print('찰칵!')
        else:
            print('카메라 켜주세요!')

    def onoffCam(self, e):
        if self.camButton.isChecked():
            self.camButton.setText('CAM OFF')
            self.video.startCam()
        else:
            self.camButton.setText('CAM ON')
            self.video.stopCam()


if __name__ == '__main__':
    app = QApplication(sys.argv) # 프로그램 실행 클래스
    myWindow = MainWindow() # 객체 생성
    myWindow.show() # 프로그램 화면 출력
    sys.exit(app.exec_()) # 프로그램 종료