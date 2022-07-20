import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from threading import Thread
import time


class video(QObject):
    sendImage = pyqtSignal(QImage)

    def __init__(self, widget, size, channel):
        super().__init__()
        self.widget = widget
        self.size = size
        self.channel = channel
        self.sendImage.connect(self.widget.recvImage)

    def startCam(self):
        try:
            self.cap = cv2.VideoCapture(self.channel, cv2.CAP_DSHOW)
        except Exception as e:
            print('Cam Error : ', e)
        else:
            self.bThread = True
            self.thread = Thread(target=self.threadFunc)
            self.thread.start()

    def captureCam(self):
        try:
            myimage = 'image/image_' + time.strftime('%Y%m%d_%H%M%S') + '.jpg'
            cv2.imwrite(myimage, self.image)
        except Exception as e:
            print('Cam Error : ', e)

    def stopCam(self):
        self.bThread = False
        #bopen = False
        try:
            self.cap.release()
        except Exception as e:
            print('Error')
        #else:


    def threadFunc(self):
        while self.bThread:
            ret, img = self.cap.read()
            if ret:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                h, w, ch = img.shape
                bytesPerLine = ch * w
                qimg = QImage(img.data, w, h, bytesPerLine, QImage.Format_RGB888)
                self.sendImage.emit(qimg)
                self.image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            else:
                print('cam read error')
            time.sleep(0.01)
        print('thread finished')