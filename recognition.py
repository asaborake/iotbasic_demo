# -*- coding: utf-8 -*-
import cv2
import sys
import numpy as np
from scipy import stats

sw = 16
sh = 12

hmin = 0
hmax = 30
smin = 50

def getImageVector(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv_channels = cv2.split(hsv)
    h_channel = hsv_channels[0]
    s_channel = hsv_channels[1]
    h_binary = cv2.GaussianBlur(h_channel, (5,5), 0)
    ret,h_binary = cv2.threshold(h_binary, hmax, 255, cv2.THRESH_TOZERO_INV)
    ret,h_binary = cv2.threshold(h_binary, hmin, 255, cv2.THRESH_BINARY)
    ret,s_binary = cv2.threshold(s_channel, smin, 255, cv2.THRESH_BINARY)
    hs_and = h_binary & s_binary
    img_dist, img_label = cv2.distanceTransformWithLabels(255-hs_and, cv2.cv.CV_DIST_L2, 5)
    img_label = np.uint8(img_label) & hs_and
    img_label_not_zero = img_label[img_label != 0]
    if len(img_label_not_zero) != 0:
        m = stats.mode(img_label_not_zero)[0]
    else:
        m = 0
    hand = np.uint8(img_label == m)*255
    nonzero = cv2.findNonZero(hand)
    xx, yy, ww, hh = cv2.boundingRect(nonzero)
    img_nonzero = hand[yy:yy+hh, xx:xx+ww]
    img_small = np.zeros((sh, sw), dtype=np.uint8)
    if 4*hh < ww*3 and hh > 0:
        htmp = int(sw*hh/ww)
        if htmp>0:
            img_small_tmp = cv2.resize(img_nonzero, (sw, htmp), interpolation=cv2.INTER_LINEAR)
            img_small[(sh-htmp)/2:(sh-htmp)/2+htmp, 0:sw] = img_small_tmp
    elif 4*hh >= ww*3 and ww > 0:
        wtmp = int(sh*ww/hh)
        if wtmp>0:
            img_small_tmp = cv2.resize(img_nonzero, (wtmp, sh), interpolation=cv2.INTER_LINEAR)
            img_small[0:sh, (sw-wtmp)/2:(sw-wtmp)/2+wtmp] = img_small_tmp
    return np.array([img_small.ravel()/255.])