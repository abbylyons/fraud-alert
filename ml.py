import numpy as np
from sklearn import svm
from sklearn.externals import joblib

# Do initial training on an account
def fit(charges):
	# train and pickle our data
	clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
	clf.fit(charges)
	joblib.dump(clf, 'train.pkl')

# Classify a new charge
def classify_new(new_charge):
	clf = joblib.load('train.pkl') 
	return clf.predict([new_charge])  # if prediction is -1, send out charge