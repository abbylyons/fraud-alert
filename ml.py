import numpy as np
from sklearn import svm
from sklearn.externals import joblib

class Svm(object):
	def __init__(self, filename):
		self.file = filename
		if os.path.isfile(filename):
			self.clf = joblib.load(filename)
		else:
			self.clf = None

    def refit(self, charges):
    	self.clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
    	self.clf.fit(charges)
    	joblib.dump(clf, self.file)

	def classify_new(self, new_charge):
		if self.clf == None:
			print "Tried to classify with no model"
		else:
			return self.clf.predict([new_charge])