import random
import numpy as np
import csv_file_reader
from sklearn import svm
from sklearn.cross_validation import KFold

#TODO Incorporate artist somehow - maybe add it to a list and include a 'count' for the amount of itmes included
def constructData(dataset, binaryClass):
	for d in dataset:
		if d:
			allFeatures = True
			for feature in d.values():
				if feature == '':
					allFeatures = False
			if allFeatures:
				data.append( [ int(d['key']), int(d['mode']), float(d['tempo']), int(d['time_signature']), float(d['duration']), float(d['danceability']), float(d['acousticness']), \
					float(d['instrumentalness']), float(d['speechiness']), float(d['loudness']), float(d['liveness']), float(d['valence']) ] )
				categories.append(binaryClass)

def performKFold(name, svc, n_folds):
	scores = []
	fold = KFold(len(categories), n_folds)

	for k, (train, test) in enumerate(fold):
		print ("Fold %d: " % k)
		svc.fit(data[train], categories[train])
		print ("Predictions: ")
		print (svc.predict(data[test]))
		scores.append(svc.score(data[test], categories[test]))

	print (name + ": " + str(scores))
	print ("Mean: " + str(np.mean(scores)))

data = []
categories = []

constructData(csv_file_reader.data_set, 1)
constructData(csv_file_reader.dislike_data_set, 0)

data = np.array(data)
categories = np.array(categories)


C = 1.0 										# SVM regularization parameter
k_folds = 10									# Number of cross validation folds
svc = svm.SVC(kernel='linear', C=C)
lin_svc = svm.LinearSVC(C=C)
rbf_svc = svm.SVC(kernel='rbf', gamma=0.7, C=C)
#poly_svc = svm.SVC(kernel='poly', degree=3, C=C) # This pauses execution on lin_svc fold 8 for some reason

performKFold('svc', svc, k_folds)
performKFold('lin_svc', lin_svc, k_folds)
performKFold('rbf_svc', rbf_svc, k_folds)
#performKFold('poly_svc', poly_svc, k_folds)


