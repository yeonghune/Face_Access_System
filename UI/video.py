from PyQt5.QtCore import pyqtSignal, QThread
import cv2
import numpy as np

# QThread 스래드 활성화
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray, bool)
    def __init__(self, disply_width, display_height):
        super().__init__()
        self._run_flag = True
        self.disply_width = disply_width
        self.display_height = display_height

    #opencv 실행
    def run(self):
        cap = cv2.VideoCapture(0)
        # opencv 카메라 화질 설정
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 672)
        cap.set(cv2.CAP_PROP_FPS, 20)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 378)
        
        try:
            while self._run_flag:
                ret, cv_img = cap.read()
                # UI 사이즈랑 맟주기 위해 행렬 자르기
                cv_img = cv_img[4:self.display_height+4, 90:self.disply_width+90]
                
                if ret:
                    # pyqt에서 지원하는 사용자 정의 시그널
                    self.change_pixmap_signal.emit(cv_img, ret)
        except:
            print("카메라를 확인하세요")
        cap.release()
        
    #opencv 멈춤
    def stop(self):
        self._run_flag = False
        self.wait()