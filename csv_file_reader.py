# Python 3.5.1
# This code reads in a csv file and converts the data into a list of dictionaries.
# Where each dictionary represents a song and its attributes.
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

import csv

data = [[]]
dislike_data = [[]]

data_set = []
dislike_data_set = []

#Reads in a csv file, converts to dictionary
def readDataset(filename, data, data_set):
	with open(filename, newline='') as file:
		i = 1
		reader = csv.reader(file)
		for row in reader:
			if (len(row) != 0):
				data.append(row)
				data_set.append({'title': data[i][0], 'artist': data[i][1], 'acousticness': data[i][2], \
				 	'danceability': data[i][3], 'duration': data[i][4], 'energy': data[i][5], 'instrumentalness': data[i][6], \
				 	'key': data[i][7], 'liveness': data[i][8], 'loudness': data[i][9], 'mode': data[i][10], 'speechiness': data[i][11], \
				 	'tempo': data[i][12],'time_signature': data[i][13], 'valence': data[i][14]})
				i += 1

readDataset('spotify_dataset.csv', data, data_set)
readDataset('spotify_dislike_dataset.csv', dislike_data, dislike_data_set)

'''
with open('spotify_dataset.csv', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        if len(row) != 0:
            data[0] = row
            data_set.append({'title': data[0][0], 'artist': data[0][1], 'acousticness': data[0][2], 'danceability': data[0][3], 'duration': data[0][4], 'energy': data[0][5], 'instrumentalness': data[0][6], 'key': data[0][7], 'liveness': data[0][8], 'loudness': data[0][9], 'mode': data[0][10], 'speechiness': data[0][11], 'tempo': data[0][12],'time_signature': data[0][13], 'valence': data[0][14]})

'''