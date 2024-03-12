from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtTest import *
import requests

URL = "http://192.168.0.4:3000/checkMember"

# loding_animation 스래드
class ICommunication(QThread):
    ICommunication_signal = pyqtSignal(str)
    def __init__(self, Id):
        super().__init__()
        self._run_flag = True
        self.data = {}
        self.data['pin'] = Id

    #스래드에서 실행될 동작
    def run(self):
        if self._run_flag:
            try:
                self.ICommunication_signal.emit(None)
                response = requests.post(URL, json=self.data)
                print(response.text)
                
                QTest.qWait(1000)

                self.ICommunication_signal.emit(response.text)
                
            except:
                self.ICommunication_signal.emit('False')
        else:
            self.ICommunication_signal.emit('False')

    #동작 멈춤
    def stop(self):
        self._run_flag = False
        self.wait()