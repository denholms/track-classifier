import csv
from sklearn.ensemble import RandomForestClassifier
from random import shuffle

data = [[]]
data_set = []
target = []

with open('spotify_dataset.csv') as file:
    reader = csv.reader(file)
    for row in reader:
        data[0] = row
        # excludes title, artist from the data set
        data_set.append([float(i) for i in data[0][2:]])
        # makes a column of 1s since these are 'liked' tracks
        target.append(1)

with open('spotify_dislike_dataset.csv') as file:
    reader = csv.reader(file)
    for row in reader:
        data[0] = row
        # excludes title, artist from the data set
        data_set.append([float(i) for i in data[0][2:]]) 
        # makes a column of 0s since these are 'liked' tracks
        target.append(0)

# groups (data_set, target) so that they can be shuffled together
zipped = list(zip(data_set, target))

shuffle(zipped)

# turns data_set and target to their own arrays
data_set, target = zip(*zipped)

classifier = RandomForestClassifier()

score = 0
size = len(data_set)
interval = size / 10

k = 10
folded_data_set = []
folded_target = []

# split into k folds
for i in range(k):
    folded_data_set.append(list(data_set[i * interval:(i + 1) * interval]))
    folded_target.append(list(target[i * interval:(i + 1) * interval]))

for i in range(0, k):
    # adding all folds before and after validation fold, e.g. folds 0 to 4 + folds 5 to k
    training_X = sum(folded_data_set[0:k - 1 - i], []) + sum(folded_data_set[k - i:k], [])
    training_y = sum(folded_target[0:k - 1 - i], []) + sum(folded_target[k - i:k], [])
    classifier.fit(training_X, training_y)

    validation_X = folded_data_set[k - 1 - i]
    validation_y = folded_target[k - 1 - i]
    score += classifier.score(validation_X, validation_y)

print score/k