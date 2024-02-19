from PyQt5 import QtGui, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSlot, Qt
from button_str_event import Event
from video import VideoThread
from text_animation import TextAnimation
import numpy as np
import time
import sys
import cv2
import requests
import threading

URL = "http://220.69.240.148:26999/receive"

class App(QWidget):
    button = []
    click_event = Event()
    guest_UI_trigger = False
    Ready = False
    face_cascade = cv2.CascadeClassifier('UI\haarcascade_frontface.xml')
    Face_Detected = False
    status = False
    Dont_capture = False
    def __init__(self):
        super().__init__()
        ##### 개발할때는 아래 코드를 주석처리 하는걸 권장함 #####
        #self.setWindowFlag(Qt.FramelessWindowHint)

        ##### 생성과 관련된 코드 #####
        # opencv UI 화면 크기
        self.disply_width = 480
        self.display_height = 370

        self.setWindowTitle(("얼굴 인식 출입체계"))
        self.setObjectName("Form")
        self.resize(800, 480)

        # loading animation 출력 Label
        self.loading = QtWidgets.QLabel(self)
        self.loading.setGeometry(QtCore.QRect(0, 190, 480, 150))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(83)
        self.loading.setFont(font)
        self.loading.setObjectName("loading")
        self.loading.setAlignment(QtCore.Qt.AlignCenter)
        self.loading.setText(("loading"))

        # opencv 출력 Label
        self.video = QtWidgets.QLabel(self)
        self.video.resize(self.disply_width, self.display_height)
        self.video.setGeometry(QtCore.QRect(10, 80, self.disply_width, self.display_height))
        self.video.setObjectName("video")
        
        # 나머지 Label 생성 및 디자인
        self.member_id = QtWidgets.QLabel(self)
        self.member_id.setGeometry(QtCore.QRect(500, 10, 90, 60))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.member_id.setFont(font)
        self.member_id.setAlignment(QtCore.Qt.AlignCenter)
        self.member_id.setObjectName("member_id")
        self.member_id.setStyleSheet("background-color: white; border: 1px solid #ced4da;")
        self.member_id.setText(("회원\n번호"))

        self.member_id_text = QtWidgets.QLabel(self)
        self.member_id_text.setGeometry(QtCore.QRect(590, 10, 200, 60))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(48)
        self.member_id_text.setFont(font)
        self.member_id_text.setObjectName("member_id_text")
        self.member_id_text.setStyleSheet("background-color: white; border: 1px solid #ced4da;")

        self.notification = QtWidgets.QLabel(self)
        self.notification.setGeometry(QtCore.QRect(10, 455, 480, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.notification.setFont(font)
        self.notification.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.notification.setObjectName("notification")
        self.notification.setText(("손님일 경우 0000을 누른 후 확인을 눌러주세요."))

        self.vision_logo = QtWidgets.QLabel(self)
        self.vision_logo.setGeometry(QtCore.QRect(5, 0, 490, 70))
        font = QtGui.QFont()
        font.setPointSize(6)
        self.vision_logo.setFont(font)
        self.vision_logo.setPixmap(QtGui.QPixmap("image/embedded_vision.png"))
        self.vision_logo.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.vision_logo.setObjectName("vision_logo")

        # 버튼 생성
        self.button_design(600, 380, 0)
        self.button_design(500, 80, 1)
        self.button_design(600, 80, 2)
        self.button_design(700, 80, 3)
        self.button_design(500, 180, 4)
        self.button_design(600, 180, 5)
        self.button_design(700, 180, 6)
        self.button_design(500, 280, 7)
        self.button_design(600, 280, 8)
        self.button_design(700, 280, 9)
        self.button_design(700, 380, 10)
        self.button_design(500, 380, 11)
        self.button_design(1500, 0, 12)

        # 버튼에 이벤트 적용
        self.button[0].clicked.connect(self.click_event.zero)
        self.button[0].clicked.connect(self.id_text_update)
        self.button[0].clicked.connect(self.button_trigger)
        
        self.button[1].clicked.connect(self.click_event.one)
        self.button[1].clicked.connect(self.id_text_update)
        self.button[1].clicked.connect(self.button_trigger)

        self.button[2].clicked.connect(self.click_event.two)
        self.button[2].clicked.connect(self.id_text_update)
        self.button[2].clicked.connect(self.button_trigger)

        self.button[3].clicked.connect(self.click_event.three)
        self.button[3].clicked.connect(self.id_text_update)
        self.button[3].clicked.connect(self.button_trigger)

        self.button[4].clicked.connect(self.click_event.four)
        self.button[4].clicked.connect(self.id_text_update)
        self.button[4].clicked.connect(self.button_trigger)

        self.button[5].clicked.connect(self.click_event.five)
        self.button[5].clicked.connect(self.id_text_update)
        self.button[5].clicked.connect(self.button_trigger)

        self.button[6].clicked.connect(self.click_event.six)
        self.button[6].clicked.connect(self.id_text_update)
        self.button[6].clicked.connect(self.button_trigger)

        self.button[7].clicked.connect(self.click_event.seven)
        self.button[7].clicked.connect(self.id_text_update)
        self.button[7].clicked.connect(self.button_trigger)

        self.button[8].clicked.connect(self.click_event.eight)
        self.button[8].clicked.connect(self.id_text_update)
        self.button[8].clicked.connect(self.button_trigger)

        self.button[9].clicked.connect(self.click_event.nine)
        self.button[9].clicked.connect(self.id_text_update)
        self.button[9].clicked.connect(self.button_trigger)

        self.button[10].clicked.connect(self.enter_event)

        self.button[11].clicked.connect(self.click_event.delete)
        self.button[11].clicked.connect(self.id_text_update)
        self.button[11].clicked.connect(self.button_trigger)

        self.button[12].clicked.connect(self.main_UI)

        ##### 스래드 실행 코드 #####
        # video 스래드 실행
        self.video_thread = VideoThread(self.disply_width, self.display_height)
        self.video_thread.change_pixmap_signal.connect(self.update_image)
        self.video_thread.start()

        # loading animation 스래드 실행
        self.loading_thread = TextAnimation()
        self.loading_thread.text_animation_signal.connect(self.update_text)
        self.loading_thread.start()
        
        QtCore.QMetaObject.connectSlotsByName(self)
        
    # 손님용 UI
    # 주의: 나이에 대한 정보는 self.click_event.number에 담겨짐
    def guest_UI(self):
        self.member_id.setText(("나이"))
        self.notification.setText(("자신의 나이를 누른 후 확인을 눌러주세요."))
        self.click_event.number = ""
        self.member_id_text.setText(f"{self.click_event.number}")
        self.button[11].setGeometry(QtCore.QRect(1500, 0, 90, 90))
        self.button[12].setGeometry(QtCore.QRect(500, 380, 90, 90))
        self.guest_UI_trigger = True
        self.repaint()
    
    #메인 UI
    # 주의: 회원 정보는 self.click_event.number에 담겨짐
    def main_UI(self):
        self.guest_UI_trigger = False
        self.button[0].setGeometry(QtCore.QRect(600, 380, 90, 90))
        self.button[1].setGeometry(QtCore.QRect(500, 80, 90, 90))
        self.button[2].setGeometry(QtCore.QRect(600, 80, 90, 90))
        self.button[3].setGeometry(QtCore.QRect(700, 80, 90, 90))
        self.button[4].setGeometry(QtCore.QRect(500, 180, 90, 90))
        self.button[5].setGeometry(QtCore.QRect(600, 180, 90, 90))
        self.button[6].setGeometry(QtCore.QRect(700, 180, 90, 90))
        self.button[7].setGeometry(QtCore.QRect(500, 280, 90, 90))
        self.button[8].setGeometry(QtCore.QRect(600, 280, 90, 90))
        self.button[9].setGeometry(QtCore.QRect(700, 280, 90, 90))
        self.button[10].setGeometry(QtCore.QRect(700, 380, 90, 90))
        self.button[11].setGeometry(QtCore.QRect(500, 380, 90, 90))
        self.button[12].setGeometry(QtCore.QRect(1500, 0, 90, 90))
        self.video.setGeometry(QtCore.QRect(10, 80,  self.disply_width, self.display_height))
        self.member_id.setGeometry(QtCore.QRect(500, 10, 90, 60))
        self.member_id_text.setGeometry(QtCore.QRect(590, 10, 200, 60))
        self.notification.setGeometry(QtCore.QRect(10, 455, 480, 20))
        self.vision_logo.setGeometry(QtCore.QRect(5, 0, 490, 70))
        self.loading.setGeometry(QtCore.QRect(1500, 0, 800, 480))
        self.member_id.setText(("회원\n번호"))

        if not self.Ready:
            self.notification.setText(("손님일 경우 0000을 누른 후 확인을 눌러주세요."))
            self.click_event.number = ""
        
        if self.Face_Detected:
            self.Face_Detected = False
            self.Dont_capture = True
            self.video.setGeometry(QtCore.QRect(1500, 0,  self.disply_width, self.display_height))
            self.loading.setGeometry(QtCore.QRect(0, 190, 480, 150))
            communication_thread = threading.Thread(target=self.Transmission, args=(self.click_event.number, self.roi_color))
            communication_thread.start()

        self.member_id_text.setText(f"{self.click_event.number}")
        #self.repaint()
    
    def Transmission(self, Id, img):
        data = {}
        self.notification.setText(("잠시만 기다려 주십시오."))
        self.notification
        data['Id'] = Id
        data['Face'] = img.tolist()
        response = requests.post(URL, json = data)
        print(response.text)
        if response.text == 'True':
            self.status = True
            self.Ready = False
            self.Dont_capture = False
            self.main_UI()
    
    # 확인버튼 이벤트
    # 주의:통신으로 정보가 넘어간후 main_UI()를 통해 원상 복구를 해야함으로, 통신이 끝났음에 대한 trigger가 존재 해야함 
    def enter_event(self):
        change = 1500
        if(self.click_event.number == "0000"):
            self.guest_UI()
        else:
            self.Ready = True
            self.notification.setText("두 사각형을 최대한 겹치게 해주세요")

            
            self.repaint()

            # time.sleep 사용시 스래드가 멈춤
            # 유사한 기능을 구현하기 위해 time.sleep를 사용함
            self.main_UI()

    
    # 뒤로 버튼과 삭제버튼 교환 기능
    def button_trigger(self):
        if(self.guest_UI_trigger == True):
            if(self.click_event.number == ""):
                self.button[12].setGeometry(QtCore.QRect(500, 380, 90, 90))
                self.button[11].setGeometry(QtCore.QRect(1500, 0, 90, 90))
                self.repaint()
            else:
                self.button[12].setGeometry(QtCore.QRect(1500, 0, 90, 90))
                self.button[11].setGeometry(QtCore.QRect(500, 380, 90, 90))
                self.repaint()

    # 버튼 디자인
    def button_design(self, x, y, index):
        self.button.insert(index, QtWidgets.QPushButton(self))
        self.button[index].setGeometry(QtCore.QRect(x, y, 90, 90))
        font = QtGui.QFont()
        font.setFamily("Arial")
        if(index < 10):
            font.setPointSize(48)
            self.button[index].setText(f"{index}")
        elif(index == 10):
            font.setPointSize(24)
            self.button[index].setText("확인")
        elif(index == 11):
            font.setPointSize(24)
            self.button[index].setText("삭제")  
        elif(index == 12):
            font.setPointSize(24)
            self.button[index].setText("뒤로")
        else:
            print("수동으로 text를 지정하세요")
        self.button[index].setFont(font)
        self.button[index].setObjectName(f"button{index}")
    
    # member_id_text의 text업데이트
    def id_text_update(self):
        self.member_id_text.setText(f"{self.click_event.number}")
        self.member_id_text.repaint()
    
    # video 스래드 값을 받아옴
    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.video.setPixmap(qt_img)

    # text animation 스래드 값을 받아옴
    @pyqtSlot(int)
    def update_text(self, count):
        if(count == 0):
            self.loading.setText(("loading"))
            self.repaint()
        if(count == 1):
            self.loading.setText(("loading."))
            self.repaint()
        if(count == 2):
            self.loading.setText(("loading.."))
            self.repaint()
        if(count == 3):
            self.loading.setText(("loading..."))
            self.repaint()

    # opencv 화면 출력시 필요한 부분
    # 주의: 원본 이미지에 대한 정보는 video 클래스에서 처리해야 함
    def convert_cv_qt(self, cv_img):
        
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        origin = rgb_image[:,:].copy()
        h, w, ch = rgb_image.shape #(360, 480, 3)
        if self.Ready == True and self.Dont_capture == False:
            box1 = [150, 80, 330, 260]
            gray = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY)
            cv2.rectangle(rgb_image, (150, 80), (330, 260), (0, 0, 0), 2)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

            if len(faces) == 1:
                x, y, width, height = faces[0, 0], faces[0, 1], faces[0, 2], faces[0, 3]
                cv2.rectangle(rgb_image,(x,y),(x+width,y+height),(255,0,0),2)
                box2 = [x, y, x+height, y+width]
                
                box1_area = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
                box2_area = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)

                # obtain x1, y1, x2, y2 of the intersection
                x1 = max(box1[0], box2[0])
                y1 = max(box1[1], box2[1])
                x2 = min(box1[2], box2[2])
                y2 = min(box1[3], box2[3])

                # compute the width and height of the intersection
                Width = max(0, x2 - x1 + 1)
                Height = max(0, y2 - y1 + 1)

                inter = Width * Height
                iou = inter / (box1_area + box2_area - inter)
                print(iou)

                if iou > 0.75:
                    self.roi_color = origin[y:y+height, x:x+width]
                    self.Face_Detected = True
                    self.main_UI()


            if len(faces) >= 2:
                print("얼굴이 두명")


        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

if __name__=="__main__":
    app = QApplication(sys.argv)
    appMain = App()
    appMain.show()
    sys.exit(app.exec_())