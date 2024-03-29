from PyQt5 import QtGui, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSlot, Qt
from button_str_event import Event
from video import VideoThread
from text_animation import TextAnimation
from FCommunication import FCommunication
from ICommunication import ICommunication
from GCommunication import GCommunication
from PyQt5.QtTest import *
import numpy as np
import sys
import cv2
import tensorflow as tf
from tensorflow import keras

class App(QWidget):
    button = []
    model = keras.models.load_model('21-0.0816.h5')
    click_event = Event()
    # guest_UI 실행될때
    guest_UI_trigger = False
    # 얼굴인식 켜기
    capture_trigger = False
    # 카메라가 켜질때
    ret_trigger = True
    # 삼각형 회면 켜기
    Find_Face_trigger = False
    # 얼굴을 찾았을때
    Face_Detected_trigger = False

    face_cascade = cv2.CascadeClassifier('haarcascade_frontface.xml')
    status = False
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

        self.O_img = QtWidgets.QLabel(self)
        self.O_img.setGeometry(QtCore.QRect(1500, 0, 240, 240))
        font = QtGui.QFont()
        font.setPointSize(6)
        self.O_img.setFont(font)
        self.O_img.setPixmap(QtGui.QPixmap("image/O_img.png"))
        self.O_img.setAlignment(QtCore.Qt.AlignCenter)
        self.O_img.setObjectName("O_img")
        
        self.X_img = QtWidgets.QLabel(self)
        self.X_img.setGeometry(QtCore.QRect(1500, 0, 240, 240))
        font = QtGui.QFont()
        font.setPointSize(6)
        self.X_img.setFont(font)
        self.X_img.setPixmap(QtGui.QPixmap("image/X_img.png"))
        self.X_img.setAlignment(QtCore.Qt.AlignCenter)
        self.X_img.setObjectName("X_img")

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

        self.button[12].clicked.connect(self.back_event)
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

        self.button_Disa(True)
        
        QtCore.QMetaObject.connectSlotsByName(self)
        
    ##### 상호작용을 위한 함수들 #####
        
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
        self.O_img.setGeometry(QtCore.QRect(1500, 0, 240, 240))
        self.X_img.setGeometry(QtCore.QRect(1500, 0, 240, 240))

        if self.Find_Face_trigger == True:
            self.button_Disa(True)
            self.button[12].setGeometry(QtCore.QRect(500, 380, 90, 90))
            self.button[11].setGeometry(QtCore.QRect(1500, 0, 90, 90))
        
        elif self.Find_Face_trigger == False:
            self.notification.setText(("손님일 경우 0000을 누른 후 확인을 눌러주세요."))
            self.click_event.number = ""
            self.button_Disa(False)

        if self.Face_Detected_trigger == True:
            self.button_Disa(True)
            self.Face_Detected_trigger = False
            self.capture_trigger = True
            self.video.setGeometry(QtCore.QRect(1500, 0,  self.disply_width, self.display_height))
            self.loading.setGeometry(QtCore.QRect(0, 190, 480, 150))
            # FCommunication 스래드 실행
            self.FCommunication_thread = FCommunication(self.click_event.number, self.roi_color)
            self.FCommunication_thread.FCommunication_signal.connect(self.FTransmission)
            self.FCommunication_thread.start()

        self.member_id_text.setText(f"{self.click_event.number}")
        self.repaint()

    # 손님용 UI
    # 주의: 나이에 대한 정보는 self.click_event.number에 담겨짐
    def guest_UI(self):
        self.member_id.setText(("나이"))
        self.notification.setText(("자신의 나이를 누른 후 확인을 눌러주세요."))
        self.member_id_text.setText(f"{self.click_event.number}")
        self.button_exchange("back")
        self.guest_UI_trigger = True
        
        if self.Find_Face_trigger == True:
            self.button_Disa(True)
            self.button_exchange("back")
            self.button[12].setEnabled(True)
        
        elif self.Find_Face_trigger == False:
            self.click_event.number = ""

        if self.Face_Detected_trigger == True:
            self.button_Disa(True)
            self.Face_Detected_trigger = False
            self.capture_trigger = True
            self.video.setGeometry(QtCore.QRect(1500, 0,  self.disply_width, self.display_height))
            self.loading.setGeometry(QtCore.QRect(0, 190, 480, 150))

            Input = self.roi_color/255
            Input = np.expand_dims(Input, axis = 0)
            pred = self.model.predict(Input)
            # print(pred[0][0])
            ## 이상1>0.5 나이, 성별
            # FCommunication 스래드 실행
            self.GCommunication_thread = GCommunication(self.click_event.number, pred[0][0])
            self.GCommunication_thread.GCommunication_signal.connect(self.GTransmission)
            self.GCommunication_thread.start()
            self.Find_Face_trigger = False
            self.capture_trigger = False
            self.loading.setGeometry(QtCore.QRect(1500, 0, 800, 480))
            self.O_img.setGeometry(QtCore.QRect(120, 150, 240, 240))
            self.notification.setText(("완료되었습니다."))
            QTest.qWait(2000)
            self.GCommunication_thread.stop()

            self.main_UI()

        self.repaint()
        
    # 확인버튼 이벤트
    def enter_event(self):
        if self.click_event.number == "":
            self.notification.setText(("번호를 입력하세요."))
            
        else:
            if self.click_event.number == "0000":
                self.guest_UI()
            else:
                self.Find_Face_trigger = True
                if self.guest_UI_trigger == False:
                    self.ICommunication_thread = ICommunication(self.click_event.number)
                    self.ICommunication_thread.ICommunication_signal.connect(self.ITransmission)
                    self.ICommunication_thread.start() 
                self.repaint()

            if self.guest_UI_trigger == True:
                self.guest_UI()
            elif self.guest_UI_trigger == False:
                self.main_UI()

    # 뒤로 버튼과 삭제버튼 교환 하기 위한 버튼 이벤트 추적
    def button_trigger(self):
        if self.guest_UI_trigger == True:
            if self.click_event.number == "":
                self.button_exchange("back")
            else:
                self.button_exchange("delete")

    # 뒤로 버튼과 삭제버튼 교환
    def button_exchange(self, state):
        if state == "back":
            self.button[12].setGeometry(QtCore.QRect(500, 380, 90, 90))
            self.button[11].setGeometry(QtCore.QRect(1500, 0, 90, 90))
            self.repaint()
        elif state == "delete":
            self.button[12].setGeometry(QtCore.QRect(1500, 0, 90, 90))
            self.button[11].setGeometry(QtCore.QRect(500, 380, 90, 90))
            self.repaint()

    # 버튼 디자인
    def button_design(self, x, y, index):
        self.button.insert(index, QtWidgets.QPushButton(self))
        self.button[index].setGeometry(QtCore.QRect(x, y, 90, 90))
        font = QtGui.QFont()
        font.setFamily("Arial")
        if index < 10:
            font.setPointSize(48)
            self.button[index].setText(f"{index}")
        elif index == 10:
            font.setPointSize(24)
            self.button[index].setText("확인")
        elif index == 11:
            font.setPointSize(24)
            self.button[index].setText("삭제")  
        elif index == 12:
            font.setPointSize(24)
            self.button[index].setText("뒤로")
        else:
            print("수동으로 text를 지정하세요")
        self.button[index].setFont(font)
        self.button[index].setObjectName(f"button{index}")
    
    # 버튼 활성화 및 비활성화
    def button_Disa(self, change):
        for i in range(0, 13):
            if(change == True):
                self.button[i].setDisabled(True)
            if(change == False):
                self.button[i].setEnabled(True)

    # member_id_text의 text업데이트
    def id_text_update(self):
        self.member_id_text.setText(f"{self.click_event.number}")
        self.member_id_text.repaint()
    
    # Find_Face_trigger를 False로 바꾸는 함수
    def back_event(self):
        if self.guest_UI_trigger == False:
            self.ICommunication_thread.stop()
        self.Find_Face_trigger = False
    
    ##### 스래드 값 관리하는 함수 #####
    # video 스래드 값을 받아옴
    @pyqtSlot(np.ndarray, bool)
    def update_image(self, cv_img, ret):
        if(ret and self.ret_trigger):
            self.ret_trigger = False
            self.button_Disa(False)
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

    # FCommunication 스래드 값을 받아옴
    @pyqtSlot(str)
    def FTransmission(self, trigger):
        self.notification.setText(("잠시만 기다려 주십시오."))
        print(trigger)
        if trigger == 'True':
            self.status = True
            self.Find_Face_trigger = False
            self.capture_trigger = False
            self.loading.setGeometry(QtCore.QRect(1500, 0, 800, 480))
            self.O_img.setGeometry(QtCore.QRect(120, 150, 240, 240))
            self.notification.setText(("완료되었습니다."))
            self.FCommunication_thread.stop()

            QTest.qWait(2000)
            self.main_UI()
        elif trigger == 'False':
            self.status = True
            self.Find_Face_trigger = False
            self.capture_trigger = False
            self.loading.setGeometry(QtCore.QRect(1500, 0, 800, 480))
            self.X_img.setGeometry(QtCore.QRect(120, 150, 240, 240))
            self.notification.setText(("회원이 아닙니다."))
            QTest.qWait(1000)
            self.main_UI()
        else:
            self.status = True
            self.Find_Face_trigger = False
            self.capture_trigger = False
            self.loading.setGeometry(QtCore.QRect(1500, 0, 800, 480))
            self.X_img.setGeometry(QtCore.QRect(120, 150, 240, 240))
            self.notification.setText(("서버에 오류가 있습니다."))
            QTest.qWait(1000)
            self.main_UI()

    @pyqtSlot(str)
    def ITransmission(self, trigger):
        self.notification.setText(("잠시만 기다려 주십시오."))
        self.video.setGeometry(QtCore.QRect(1500, 0,  self.disply_width, self.display_height))
        self.loading.setGeometry(QtCore.QRect(0, 190, 480, 150))
        print("작동중")
        if trigger == 'true':
            self.button[12].setEnabled(True)
            self.notification.setText("두 사각형을 최대한 겹치게 해주세요")
            self.video.setGeometry(QtCore.QRect(10, 80,  self.disply_width, self.display_height))
            self.loading.setGeometry(QtCore.QRect(1500, 0, 800, 480))
        elif trigger == 'false':
            self.Find_Face_trigger = False
            self.loading.setGeometry(QtCore.QRect(1500, 0, 800, 480))
            self.X_img.setGeometry(QtCore.QRect(120, 150, 240, 240))
            self.notification.setText(("회원이 아닙니다."))
            QTest.qWait(1000)
            self.main_UI()
        elif trigger == 'start':
            pass
        else:
            self.Find_Face_trigger = False
            self.loading.setGeometry(QtCore.QRect(1500, 0, 800, 480))
            self.X_img.setGeometry(QtCore.QRect(120, 150, 240, 240))
            self.notification.setText(("서버에 오류가 있습니다."))
            QTest.qWait(1000)
            self.main_UI()
            
    @pyqtSlot(bool)
    def GTransmission(self, trigger):
        print(trigger)
        
        

    ##### 이미지 관리 #####
    # opencv 화면 출력시 필요한 부분
    # 주의: 원본 이미지에 대한 정보는 video 클래스에서 처리해야 함
    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        origin = rgb_image[:,:].copy()
        h, w, ch = rgb_image.shape #(360, 480, 3)
        if self.Find_Face_trigger == True and self.capture_trigger == False: 
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

                if iou > 0.75:
                    self.roi_color = origin[y:y+height, x:x+width]
                    self.roi_color = cv2.resize(self.roi_color, (112, 112))
                    self.roi_color = cv2.cvtColor(self.roi_color, cv2.COLOR_BGR2RGB)
                    self.Face_Detected_trigger = True
                    if self.guest_UI_trigger == False:
                        self.ICommunication_thread.stop()

                    if (self.guest_UI_trigger):
                        self.guest_UI()
                    else:
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