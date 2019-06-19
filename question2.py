# coding: UTF-8
import RPi.GPIO as GPIO
from time import sleep
import picamera
import picamera.array
import cv2
import sys

LED = 25

def lchika():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED, GPIO.OUT)
    num = 0
    while num < 6:
        GPIO.output(LED, GPIO.HIGH)
        sleep(0.1)
        GPIO.output(LED, GPIO.LOW)
        sleep(0.1)
        num += 1
    GPIO.cleanup()

cascade_path =  "/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml"
cascade = cv2.CascadeClassifier(cascade_path)
imgnum = 0

with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.resolution = (320, 240)
        
        try:
            while True:
                camera.capture(stream, 'bgr', use_video_port=True)
                gray = cv2.cvtColor(stream.array, cv2.COLOR_BGR2GRAY)
                facerect = cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=2, minSize=(30,30), maxSize=(150,150))

                if len(facerect) > 0:
                    for rect in facerect:
                        camera.capture('myimg.' + str(imgnum) + '.jpg')
                        imgnum += 1
                        lchika()

                stream.seek(0)
                stream.truncate()
        except KeyboardInterrupt:
            pass