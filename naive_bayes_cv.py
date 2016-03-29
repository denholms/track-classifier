# Naive bayes classifier for predicting whether a user will like or dislike a song.
# Based on song attributes of tracks they are known to like and tracks they are known to dislike.
import csv
import random
from sklearn import cross_validation
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import classification_report
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn import datasets

data = [[]]

# Indexes and the features they correspond to in the data set:
#       0 = 'title'
#       1 = 'artist'
#       2 = 'acousticness'
#       3 = 'danceability'
#       4 = 'duration'
#       5 = 'energy'
#       6 = 'instrumentalness'
#       7 = 'key'
#       8 = 'liveness'
#       9 = 'loudness'
#       10 = 'mode'
#       11 = 'speechiness'
#       12 = 'tempo'
#       13 = 'time_signature'
#       14 = 'valence'
#       15 = 'classification'
data_set = []
training_data = []
test_data = []

# classifications: 0 = dislike, 1 = like
training_classifications = []
test_classifications = []


# map song name and artist to assigned integer
# Index:
#       0 = corresponding index number from the data matrix (training_data or test_data)
#       1 = title
#       2 = artist
test_song_map = []
training_song_map = []

# Split likes into training data and test data from the spotify_dataset.csv file
with open('spotify_dataset.csv', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        if len(row) != 0 and row[0] != '':
            data[0] = row
            song_attr = [data[0][0], data[0][1], data[0][2], data[0][3], data[0][4],
                            data[0][5], data[0][6], data[0][7], data[0][8], data[0][9],
                            data[0][10], data[0][11], data[0][12], data[0][13], data[0][14], 1]

            data_set.append(song_attr)

            for i in range(len(song_attr)):
                    if song_attr[i] == '':
                        data_set.pop()
                        break
                        #song_attr[i] = float(0)
                    
            #if blank == 0:
            #data_set.append(song_attr)
                                   
# Split dislikes into training data and test data from the spotify_dislike_dataset.csv file
with open('spotify_dislike_dataset.csv', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        if len(row) != 0 and row[0] != '':
            data[0] = row
            song_attr = [data[0][0], data[0][1], data[0][2], data[0][3], data[0][4],
                             data[0][5], data[0][6], data[0][7], data[0][8], data[0][9],
                             data[0][10], data[0][11], data[0][12], data[0][13], data[0][14], 0]

            data_set.append(song_attr)

            for i in range(len(song_attr)):
                    if song_attr[i] == '':
                        data_set.pop()
                        break
                        #song_attr[i] = float(0)
                    
            #if blank == 0:
            #data_set.append(song_attr)

random.shuffle(data_set)

#split into training and test data (90:10)
num_test_data = int (len(data_set)*0.10)
num_training_data = len(data_set) - num_test_data

# test data
for i in range(num_test_data):
    song = data_set.pop()
    test_data.append([float(song[2]), float(song[3]), float(song[4]),
                            float(song[5]), float(song[6]), float(song[7]), float(song[8]), float(song[9]),
                            float(song[10]), float(song[11]), float(song[12]), float(song[13]), float(song[14])])
    test_classifications.append(song[15])
    test_song_map.append([song[0], song[1]])

# training data
for j in range(num_training_data):
    song = data_set.pop()
    training_data.append([float(data[0][2]), float(data[0][3]), float(data[0][4]),
                            float(data[0][5]), float(data[0][6]), float(data[0][7]), float(data[0][8]), float(data[0][9]),
                            float(data[0][10]), float(data[0][11]), float(data[0][12]), float(data[0][13]), float(data[0][14])])
    training_classifications.append(song[15])
    training_song_map.append([song[0], song[1]])

# train naive bayes classifier
clf = GaussianNB()
clf = clf.fit(training_data, training_classifications)

# predict classification of test data using cross validation
predicted = cross_validation.cross_val_predict(clf, test_data, test_classifications, cv=10)

# calculate accuracy of naive bayes classifier
accuracy = accuracy_score(test_classifications, predicted)
print ('naive bayes classifier accuracy = %s' % (accuracy))

# calculate precision of naive bayes classifier
precision = precision_score(test_classifications, predicted)
print ('naive bayes classifier precision = %s' % (precision))

# calculate recall of naive bayes classifier
recall = recall_score(test_classifications, predicted)
print ('naive bayes classifier recall = %s' % (recall))

# calculate f1_score of naive bayes classifier
f1_score = f1_score(test_classifications, predicted)
print ('naive bayes classifier f1_score = %s' % (f1_score))

# naive bayes classification report
print ('\n')
print ('----------------------------------------------------')
print ('naive bayes classification report:')
print ('----------------------------------------------------')

target_names = ['dislikes', 'likes']
report = classification_report(test_classifications, predicted, target_names=target_names)
print (report)
