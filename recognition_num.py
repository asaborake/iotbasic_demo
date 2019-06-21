# -*- coding: utf-8 -*-
from sklearn.externals import joblib
import cv2
import numpy as np

clf = joblib.load('svnResult.pk1')

def recog(img):
    size = (8,8)
    recog_img = cv2.resize(img, size)
    Ximg = np.asarray(recog_img, dtype=int)
    Ximg = 16*Ximg/255.0
    Ximg = Ximg.astype(int)
    Ximg = 16-Ximg
    X = np.array([Ximg.flatten()])
    y = clf.predict(X)
    return y