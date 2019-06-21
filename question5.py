# -*- coding: utf-8 -*-
import picamera
import picamera.array
import cv2
import time
import collections
import random
import recognition as recog

from sklearn.externals import joblib

clf = joblib.load('recognition.pk1')
hands = ['グー','チョキ','パー']
human_hands = []
jyanken_count = 0
cpu_win = 0
human_win = 0

def handRecognition(camera, stream):
    camera.resolution = (320, 240)
    camera.framerate = 15
    camera.awb_mode = 'fluorescent'

    while len(human_hands) < 6:
        camera.capture(stream, 'bgr', use_video_port=True)
        cv2.imshow('frame', stream.array)
        hand_vector = recog.getImageVector(stream.array)
        result = clf.predict(hand_vector)
        human_hands.append(result[0])
        stream.seek(0)
        stream.truncate()

    c = collections.Counter(human_hands)
    (h, num) = c.most_common()[0]

    return h

with picamera.PiCamera() as camera:
        with picamera.array.PiRGBArray(camera) as stream:
            while jyanken_count < 10:
                print('ジャンケンポン')
                time.sleep(1)
                human_hand = handRecognition(camera, stream)
                machine_hand = random.choice([0,1,2])
                print('あなたは' + hands[human_hand] + 'で、私は' + hands[machine_hand] + 'だから')

                if(human_hand == machine_hand):
                    print('あいこで、もう１回')
                elif(human_hand > machine_hand):
                    if(human_hand - machine_hand == 1):
                        print('私の勝ち')
                        cpu_win += 1
                    else:
                        print('私の負け')
                        human_win += 1
                    jyanken_count += 1
                elif(human_hand < machine_hand):
                    if(human_hand - machine_hand >= -1):
                        print('私の負け')
                        human_win += 1
                    else:
                        print('私の勝ち')
                        cpu_win += 1
                    jyanken_count += 1

if(cpu_win == human_win):
    winner = '引き分けです。'
elif(cpu_win > human_win):
    winner = '私の勝ちです。'
elif(cpu_win < human_win):
    winner = 'あなたの勝ちです。'

print('あなたの' + str(human_win) + '勝' + str(cpu_win) + '敗で' + winner)
