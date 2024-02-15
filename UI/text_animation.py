from PyQt5.QtCore import pyqtSignal, QThread
import time

# loding_animation 스래드
class TextAnimation(QThread):
    text_animation_signal = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self._run_flag = True

    #스래드에서 실행될 동작
    def run(self):
        while self._run_flag:
            self.text_animation_signal.emit(0)
            time.sleep(1)
            self.text_animation_signal.emit(1)
            time.sleep(1)
            self.text_animation_signal.emit(2)
            time.sleep(1)
            self.text_animation_signal.emit(3)
            time.sleep(1)
        
    #동작 멈춤
    def stop(self):
        self._run_flag = False
        self.wait()