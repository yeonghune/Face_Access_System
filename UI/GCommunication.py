from PyQt5.QtCore import pyqtSignal, QThread

# loding_animation 스래드
class GCommunication(QThread):
    GCommunication_signal = pyqtSignal(bool)
    def __init__(self, age, gender):
        super().__init__()
        self._run_flag = True
        self.age = age
        self.gender = gender

    #스래드에서 실행될 동작
    def run(self):
        if self._run_flag:
            print(self.age)
            print(self.gender)
            self.GCommunication_signal.emit(True)


    #동작 멈춤
    def stop(self):
        self._run_flag = False
        self.wait()