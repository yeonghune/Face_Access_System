from PyQt5.QtCore import pyqtSignal, QThread
import requests

URL = "http://220.69.240.148:26999/receive"

# loding_animation 스래드
class FCommunication(QThread):
    FCommunication_signal = pyqtSignal(str)
    def __init__(self, Id, img):
        super().__init__()
        self._run_flag = True
        self.Id = Id
        self.img = img

    #스래드에서 실행될 동작
    def run(self):
        if self._run_flag:
            try:
                data = {}
                data['Id'] = self.Id
                data['Face'] = self.img.tolist()
                response = requests.post(URL, json = data)
                print(response.text)
                self.FCommunication_signal.emit(response.text)
            except:
                self.FCommunication_signal.emit('True')

    #동작 멈춤
    def stop(self):
        self._run_flag = False
        self.wait()