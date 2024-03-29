from flask import Flask, request
from absl import app, flags, logging
from absl.flags import FLAGS
import cv2
import numpy as np
import os
import tensorflow as tf

from modules.evaluations import get_val_data, perform_val
from modules.models import ArcFaceModel
from modules.utils import set_memory_growth, load_yaml, l2_norm

app = Flask(__name__)

cfg = load_yaml('./configs/arc_res50.yaml')

model = ArcFaceModel(size=cfg['input_size'],
                    backbone_type=cfg['backbone_type'],
                    training=False)

ckpt_path = tf.train.latest_checkpoint('./checkpoints/' + cfg['sub_name'])
if ckpt_path is not None:
    print("[*] load ckpt from {}".format(ckpt_path))
    model.load_weights(ckpt_path)
else:
    print("[*] Cannot find ckpt from {}.".format(ckpt_path))
    exit()

@app.route('/receive', methods=['POST'])
def receive():
    if request.method == 'POST':
        data = request.json
        params = data['Id'] #회원번호
        img = np.array(data['Face']) #얼굴이미지
        cv2.imwrite('Input.jpg', img)

        folder = "Faces"
        route = os.path.join(folder, params)
        final_route = route + "/1.jpg"
        print(final_route)
        img = cv2.resize(img.astype('float'), (112, 112))
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img / 255
        
        if len(img.shape) == 3:
            img = np.expand_dims(img, 0)
        embeds = l2_norm(model(img))
        embeds = np.array(embeds[0])

        img2 = cv2.imread(final_route)
        img2 = cv2.resize(img2.astype('float'), (112, 112))
        img2 = img2 /255
        #img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        if len(img2.shape) == 3:
            img2 = np.expand_dims(img2, 0)
        embeds2 = l2_norm(model(img2))
        embeds2 = np.array(embeds2[0])

        print('Distance: ', np.sum(np.square(embeds - embeds2)))
        Similarity = np.dot(embeds, embeds2.T)
        print('Similarity: ', np.dot(embeds, embeds2.T))

        if Similarity > 0.4:
            Response = True
        else:
            Response = False


        return str(Response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = '0000')
