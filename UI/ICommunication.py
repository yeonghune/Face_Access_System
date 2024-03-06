from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtTest import *
import requests

URL = "http://220.69.240.148:26999/receive"

# loding_animation 스래드
class ICommunication(QThread):
    ICommunication_signal = pyqtSignal(str)
    def __init__(self, Id):
        super().__init__()
        self._run_flag = True
        self.Id = Id

    #스래드에서 실행될 동작
    def run(self):
        if self._run_flag:
            try:
                self.ICommunication_signal.emit('False')

                print("확인")
                QTest.qWait(2000)
                print("완료")

                self.ICommunication_signal.emit('True')
                
            except:
                self.ICommunication_signal.emit('False')
        else:
            self.ICommunication_signal.emit('False')

    #동작 멈춤
    def stop(self):
        self._run_flag = False
        self.wait()