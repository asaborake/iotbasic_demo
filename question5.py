# -*- coding: utf-8 -*-
import cv2
import sys
import picamera
import picamera.array

import collections
import recognition as recog
from sklearn.externals import joblib

# 学習済みモデルの読み込み
clf = joblib.load('recognition.pk1')

jyanken_hands = []
with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.resolution = (320, 240)
        camera.framerate = 15
        camera.awb_mode = 'fluorescent'

        while len(jyanken_hands) < 6:
            camera.capture(stream, 'bgr', use_video_port=True)
            hand_vector = recog.getImageVector(stream.array)
            result = clf.predict(hand_vector)
            jyanken_hands.append(result[0])
            stream.seek(0)
            stream.truncate()

        print(jyanken_hands)

        #c = collections.Counter(jyanken_hands)
        #(jyanken_hand, num) = c.most_common()[0]
        #print(jyanken_hand)

        cv2.destroyAllWindows()