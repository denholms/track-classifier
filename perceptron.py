#!/usr/bin/env python2

import csv
import numpy as np
from sklearn.linear_model import Perceptron

# Dictionary keys are:
#       'title'
#       'artist'
#       'acousticness'
#       'danceability'
#       'duration'
#       'energy'
#       'instrumentalness'
#       'key'
#       'liveness'
#       'loudness'
#       'mode'
#       'speechiness'
#       'tempo'
#       'time_signature'
#       'valence'

def load_file(filename):
    data_set = [] # list of dictionaries
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        data = [[]]
        for row in reader:
            if len(row) != 0:
                data[0] = row
                data_set.append({'title': data[0][0], 'artist': data[0][1], 'acousticness': data[0][2], 'danceability': data[0][3], 'duration': data[0][4], 'energy': data[0][5], 'instrumentalness': data[0][6], 'key': data[0][7], 'liveness': data[0][8], 'loudness': data[0][9], 'mode': data[0][10], 'speechiness': data[0][11], 'tempo': data[0][12], 'time_signature': data[0][13], 'valence': data[0][14]})

    return data_set

def remove_empty(data_raw):
    result = []
    for row in data_raw:
        add = True
        for key, value in row.items():
            if key in ['title', 'artist']:
                continue
            try:
                float(value)
            except:
                add = False
                break
        if add:
            result.append(row)

    return result

def prepare_data(data_raw):
    data = [] # list of lists
    for row in data_raw:
        # row: dictionary
        # exclude title and artist
        values = [float(value) for key, value in row.items() \
                        if key not in ['title', 'artist']]
        data.append(values)

    return data

def shuffle(data, classifications):
    shuffled_data = np.empty(data.shape, dtype=data.dtype)
    shuffled_classifications = np.empty(classifications.shape, dtype=classifications.dtype)
    permutation = np.random.permutation(len(data))
    for old_index, new_index in enumerate(permutation):
        shuffled_data[new_index] = data[old_index]
        shuffled_classifications[new_index] = classifications[old_index]
    return shuffled_data, shuffled_classifications

def k_fold(k, data, classifications, i):
    n = len(data)
    test_data = data[i*(n/k) : (i+1)*(n/k)]
    test_classifications = classifications[i*(n/k) : (i+1)*(n/k)]

    train_data = []
    train_data.extend(data[: i*(n/k)])
    train_data.extend(data[(i+1)*(n/k):])
    train_classifications = []
    train_classifications.extend(classifications[: i*(n/k)])
    train_classifications.extend(classifications[(i+1)*(n/k):])

    return test_data, test_classifications, train_data, train_classifications

def calc_accuracy(classifications, predictions):
    correct = 0
    for i in range(len(classifications)):
        if predictions[i] == classifications[i]:
            correct += 1

    return float(correct) / len(classifications)

def calc_precision(classifications, predictions, cls):
    true_pos = 1
    false_pos = 1
    for i in range(len(classifications)):
        if predictions[i] == cls and classifications[i] == cls:
            true_pos += 1

        if predictions[i] == cls and classifications[i] != cls:
            false_pos += 1

    return float(true_pos) / float(true_pos + false_pos)

def calc_recall(classifications, predictions, cls):
    true_pos = 1
    false_neg = 1
    for i in range(len(classifications)):
        if predictions[i] != cls and classifications[i] == cls:
            false_neg += 1

        if predictions[i] == cls and predictions[i] == classifications[i]:
            true_pos += 1

    return float(true_pos) / float(true_pos + false_neg)

def main():
    likes_raw = load_file('spotify_dataset.csv')
    dislikes_raw = load_file('spotify_dislike_dataset.csv')

    likes_raw = remove_empty(likes_raw)
    dislikes_raw = remove_empty(dislikes_raw)

    likes = prepare_data(likes_raw)
    dislikes = prepare_data(dislikes_raw)

    # Convert to numpy arrays
    data = np.array(likes + dislikes)
    classifications = np.array([1]*len(likes) + [0]*len(dislikes))

    data, classifications = shuffle(data, classifications)

    k = 10
    fold_size = int(len(data) * 1/float(k))

    print "N = %d" %(len(data))
    print "Using %d folds, with fold size of %d" %(k, fold_size)

    sum_accuracy = 0
    sum_like_precision = 0
    sum_like_recall = 0
    sum_dislike_precision = 0
    sum_dislike_recall = 0
    for i in range(k):
        test_data, test_classifications, train_data, train_classifications = k_fold(k, data, classifications, i)

        clf = Perceptron(penalty='l2')
        clf = clf.fit(train_data, train_classifications)

        predictions = clf.predict(test_data)

        accuracy = calc_accuracy(test_classifications, predictions)
        sum_accuracy += accuracy

        like_precision = calc_precision(test_classifications, predictions, 1)
        sum_like_precision += like_precision

        like_recall = calc_recall(test_classifications, predictions, 1)
        sum_like_recall += like_recall

        dislike_precision = calc_precision(test_classifications, predictions, 0)
        sum_dislike_precision += dislike_precision

        dislike_recall = calc_recall(test_classifications, predictions, 0)
        sum_dislike_recall += dislike_recall

    avg_accuracy = sum_accuracy / k
    print "Avg. accuracy = %s" %avg_accuracy

    avg_like_precision = sum_like_precision / k
    print "Avg. like precision = %s" %avg_like_precision

    avg_like_recall = sum_like_recall / k
    print "Avg. like recall = %s" %avg_like_recall

    avg_dislike_precision = sum_dislike_precision / k
    print "Avg. dislike precision = %s" %avg_dislike_precision

    avg_dislike_recall = sum_dislike_recall / k
    print "Avg. dislike recall = %s" %avg_dislike_recall

    avg_precision = (avg_like_precision + avg_dislike_precision) / 2
    print "Avg. precision = %s" %avg_precision

    avg_recall = (avg_like_recall + avg_dislike_recall) / 2
    print "Avg. recall = %s" %avg_recall

if __name__ == "__main__":
    main()
