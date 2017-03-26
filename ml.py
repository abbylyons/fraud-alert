import numpy as np
import os
from sklearn.externals import joblib
from sklearn.neighbors import NearestNeighbors

class Svm(object):
    def __init__(self, filename):
        self.file = filename
        if os.path.isfile(filename):
            self.clf = joblib.load(filename)
        else:
            self.clf = None

    def refit(self, charges):
        self.clf = NearestNeighbors(n_neighbors=1)
        self.clf.fit(charges)
        joblib.dump(self.clf, self.file)

    def classify_new(self, new_charges):
        if self.clf == None:
            print "Tried to classify with no model"
        else:
            return self.clf.kneighbors(new_charges)[0]
