# -*- coding: utf-8 -*-
import picamera
import picamera.array
import cv2

cascade_path = "/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml"
cascade = cv2.CascadeClassifier(cascade_path)

with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.resolution = (320, 240)

	while True:
            camera.capture(stream, 'bgr', use_video_port=True)
            gray = cv2.cvtColor(stream.array, cv2.COLOR_BGR2GRAY)

	    #二値化（白黒）
            (ret, binary) = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

	    #エッジ化（Cannyフィルタ）
            edge = cv2.Canny(gray, 50, 100)

	    #円検知（ハフ変換）
	    blur = cv2.GaussianBlur(gray, (9,9), 0)
	    circles = cv2.HoughCircles(blur, cv2.cv.CV_HOUGH_GRADIENT, dp=1, minDist=50, param1=120, param2=40, minRadius=5, maxRadius=100)
	    if circles is not None:
		for c in circles[0]:
			cv2.circle(stream.array, (c[0],c[1]), c[2], (0,0,255), 2)

	    #顔検知（カスケードファイル）
	    facerect = cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=2, minSize=(30,30), maxSize=(150,150))
	    if len(facerect) > 0:
		for rect in facerect:
			cv2.rectangle(stream.array, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), (0,0,255), thickness=2)

	    #画面表示（第２引数に表示したいものを入れる）
            cv2.imshow('frame', stream.array)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            stream.seek(0)
            stream.truncate()

	cv2.destroyAllWindows()
