# -*- coding: utf-8 -*-
import picamera
import picamera.array
import cv2

cascade_path = "./cascade.xml"
cascade = cv2.CascadeClassifier(cascade_path)

with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.resolution = (320, 240)

	while True:
            camera.capture(stream, 'bgr', use_video_port=True)
            gray = cv2.cvtColor(stream.array, cv2.COLOR_BGR2GRAY)

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
