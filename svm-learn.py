# -*- coding: utf-8 -*-
from sklearn import datasets, svm
from sklearn.externals import joblib
import numpy as np

digits = datasets.load_digits()

X = digits.data
y = digits.target

clf = svm.SVC(C=1.0, kernel='linear')
clf.fit(X, y) 

joblib.dump(clf, 'svnResult.pk1')