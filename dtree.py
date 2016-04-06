# Decision Tree Classifier for predicting a persons song likes and dislikes.
# Input: A .csv of songs liked, a .csv file of songs disliked
# Output: An accuracy score of predictions, a .dot file of the decision tree
# Note: .dot can be viewed using GVedit, found with the graphviz software
# Credit to Sarah Warnock for ideas and debugging aid from her naive_bayes_cv.py file
from sklearn import tree
import random
import csv
import numpy as np
from sklearn import cross_validation
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report



# Data indices of CSV file
#   0 = 'title'
#   1 = 'artist'
#   2 = 'acousticness'
#   3 = 'danceability'
#   4 = 'duration'
#   5 = 'energy'
#   6 = 'instrumentalness'
#   7 = 'key'
#   8 = 'liveness'
#   9 = 'loudness'
#   10 = 'mode'
#   11 = 'speechiness'
#   12 = 'tempo'
#   13 = 'time_signature'
#   14 = 'valence'


dataSet = []
data = [[]]

#Place liked data in set
with open('spotify_dataset.csv', newline='') as file:
    parser = csv.reader(file)
    for row in parser:
        if len(row) != 0 and row[0] != '':
            data[0] = row
            songValues = [data[0][2], data[0][3], data[0][4], data[0][5], data[0][6],
                          data[0][7], data[0][8], data[0][9], data[0][10], data[0][11],
                          data[0][12], data[0][13], data[0][14], 1]
            dataSet.append(songValues)

            for i in range(len(songValues)):
                    if songValues[i] == '':
                        dataSet.pop()
                        break


#Place disliked data in set
with open('spotify_dislike_dataset.csv', newline='') as file:
    parser = csv.reader(file)
    for row in parser:
        if len(row) != 0 and row[0] != '':
            data[0] = row
            songValues = [data[0][2], data[0][3], data[0][4], data[0][5], data[0][6],
                          data[0][7], data[0][8], data[0][9], data[0][10], data[0][11],
                          data[0][12], data[0][13], data[0][14], -1]
            dataSet.append(songValues)

            for i in range(len(songValues)):
                    if songValues[i] == '':
                        dataSet.pop()
                        break

# updated data indices of dataSet
#   0 = 'acousticness'
#   1 = 'danceability'
#   2 = 'duration'
#   3 = 'energy'
#   4 = 'instrumentalness'
#   5 = 'key'
#   6 = 'liveness'
#   7 = 'loudness'
#   8 = 'mode'
#   9 = 'speechiness'
#   10 = 'tempo'
#   11 = 'time_signature'
#   12 = 'valence'
#   13 = 'classification'

#Take split data and mix
random.shuffle(dataSet)

#Create folds (k=10)
k = 10
folds = int (len(dataSet) * 1/float(k))
totalDone = 0 

#Get training data
testData = []
trainData = []
testClass = []
trainClass = []

#train on first 9 folds
for i in range(folds * 9):
    attributes = dataSet.pop()
    trainData.append([float(attributes[0]), float(attributes[1]), float(attributes[2]),
                     float(attributes[3]), float(attributes[4]), float(attributes[5]),
                     float(attributes[6]), float(attributes[7]), float(attributes[8]),
                     float(attributes[9]), float(attributes[10]), float(attributes[11]),
                     float(attributes[12]),])
    trainClass.append(attributes[13])

#test on last fold
for i in range(folds * 9 +1, folds * 10):
    attributes = dataSet.pop()
    testData.append([float(attributes[0]), float(attributes[1]), float(attributes[2]),
                     float(attributes[3]), float(attributes[4]), float(attributes[5]),
                     float(attributes[6]), float(attributes[7]), float(attributes[8]),
                     float(attributes[9]), float(attributes[10]), float(attributes[11]),
                     float(attributes[12]),])
    testClass.append(attributes[13])

# Use dtree classifier
dtree = tree.DecisionTreeClassifier()
dtree = dtree.fit(trainData, trainClass)

# Predict on k=10 fold data
predictions = cross_validation.cross_val_predict(dtree, testData, testClass, cv=10)
accuracy = accuracy_score(testClass, predictions)
                
print ('Dtree accuracy = %s' % (accuracy))

tree.export_graphviz(   dtree,
                        out_file='tree.dot',
                        feature_names=[ 'acousticness','danceability','duration','energy',
                                        'instrumentalness','key','liveness','loudness','mode',
                                        'speechiness','tempo','time_signature','valence',
                                        'classification'],
                        class_names=['like','dislike'],
                        rounded=True,
                     )
