import random
import numpy as np
import csv_file_reader
from sklearn import svm
from sklearn.cross_validation import KFold
from sklearn.metrics import classification_report

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
	target_names = ['dislikes', 'likes']
	fold = KFold(len(randomizedCategories), n_folds)

	for k, (train, test) in enumerate(fold):
		print ("Fold %d: " % k)
		svc.fit(randomizedData[train], randomizedCategories[train])
		print ("Predictions: ")
		prediction =  svc.predict(randomizedData[test])
		print (prediction)
		scores.append(svc.score(randomizedData[test], randomizedCategories[test]))
		report = classification_report(randomizedCategories[test], prediction, target_names=target_names)
		print(report)

	print (name + ": " + str(scores))
	print ("Mean: " + str(np.mean(scores)))

data = []
categories = []

constructData(csv_file_reader.data_set, 1)
constructData(csv_file_reader.dislike_data_set, 0)

randomizedData = []
randomizedCategories = []

index_list = list(range(len(data)))
random.shuffle(index_list)
for index in index_list:
	randomizedData.append(data[index])
	randomizedCategories.append(categories[index])

randomizedData = np.array(randomizedData)
randomizedCategories = np.array(randomizedCategories)


C = 1.0 										# SVM regularization parameter
k_folds = 10									# Number of cross validation folds
svc = svm.SVC(kernel='linear', C=C)
lin_svc = svm.LinearSVC(C=C)
rbf_svc = svm.SVC(kernel='rbf', C=C)
nu_svc = svm.NuSVC()
#sigmoid_svc = svm.SVC(kernel='sigmoid', C=C)

performKFold('svc', svc, k_folds)
performKFold('lin_svc', lin_svc, k_folds)
performKFold('rbf_svc', rbf_svc, k_folds)
performKFold('nu_svc', nu_svc, k_folds)
#performKFold('sigmoid_svc', sigmoid_svc, k_folds)


