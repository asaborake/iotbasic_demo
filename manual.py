# -*- coding: utf-8 -*-
import picamera
import picamera.array
import cv2
import time
import collections
import recognition_num as recog

recog_numbers = []
numbers = []
repeat = 1
total = 0

with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.resolution = (320, 240)
        while repeat < 3:
            if repeat == 1:
                print('一つ目の数字をカメラに見せて')
            else:
                print('二つ目の数字をカメラに見せて')
                recog_numbers = []
                time.sleep(2)

            while len(recog_numbers) < 6:
                camera.capture(stream, 'bgr', use_video_port=True)
                gray = cv2.cvtColor(stream.array, cv2.COLOR_BGR2GRAY)
                (ret, binary) = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                number = recog.recog(binary)
                recog_numbers.append(number[0])
                stream.seek(0)
                stream.truncate()
        
            #print(recog_numbers)
            c = collections.Counter(recog_numbers)
            (h, num) = c.most_common()[0]
            numbers.append(h)
            repeat += 1
        
        for i in numbers:
            total += i
        
        print(total)