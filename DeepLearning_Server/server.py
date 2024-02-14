from flask import Flask, request
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/receive', methods=['POST'])
def receive():
    if request.method == 'POST':
        data = request.json
        params = data['Id'] #회원번호
        img = np.array(data['Face']) #얼굴이미지


        ##################################
        #   지은이가 만들어야 하는 부분    #
        ##################################





        Response = False # 신원 확인되면 True 아니면 False

        return str(Response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 26999)