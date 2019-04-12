from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from sklearn import tree
from sklearn import ensemble

import numpy as np

import flow

import re

import pickle

import os
import sys

'''
Labels:
0 - Fruit Ninja
1 - Google news
2 - Android Internet Browser
3 - The Weather Channel
4 - Youtube
'''

def main():
	argc = len(sys.argv)
	argv = sys.argv
	save = False
	load = False
	if argc > 2:
		# arg 2 should be a -s
		if argv[1] == "-s":
			save = True
			fspath = argv[2]
		elif argv[1] == "-l":
			load = True
			flpath = argv[2]
		elif arv[1] == "-h": # Repeat code, :( but its low importance
			print("Flags available: -s, -l")
			print("-s <savepath>\tSaves the classifier to that location")
			print("-l <loadpath>\tLoads in a classifier from the given path. Tests the accuracy then exits. Not useful for the project")
		if argc > 4:
			if argv[3] == "-s":
				save = True
				fspath = argv[4]
			elif argv[3] == "-l":
				load = True
				flpath = argv[4]
			elif argv[3] == "-h":
				print("Flags available: -s, -l")
				print("-s <savepath>\tSaves the classifier to that location")
				print("-l <loadpath>\tLoads in a classifier from the given path. Tests the accuracy then exits. Not useful for the project")
	# set up training set
	flowbase = "flows/" # forgot to include this in paths first time around, so i put a var here
	training_files = [
		{
			'label':0,
			'files':['flows_fn1.txt','flows_fn2.txt','flows_fn3.txt','flows_fn4.txt'],
		},
		{
			'label':1,
			'files':['flows_gnews1.txt','flows_gnews2.txt','flows_gnews3.txt','flows_gnews4.txt']
		},
		{
			'label':2,
			'files':['flows_internet1.txt','flows_internet2.txt','flows_internet3.txt','flows_internet4.txt']
		},
		{
			'label':3,
			'files':['flows_twc1.txt','flows_twc2.txt','flows_twc3.txt','flows_twc4.txt']
		},
		{
			'label':4,
			'files':['flows_youtube1.txt','flows_youtube2.txt','flows_youtube3.txt','flows_youtube4.txt']
		}
	]
	training_set = []
	training_labels = []

	# aggregate the training data along with the labels for it
	for data in training_files:
		label = data['label']
		for filepath in data['files']:
			with open(flowbase+filepath, "r") as file:
				string = find_next_flow(file)
				while not (string == -1):
					training_set.append(extract_features(parse_flow(string)))
					training_labels.append(label)
					string = find_next_flow(file)

	# set up test set
	test_files = [
		{
			'label':0,
			'files':['flows_fn5.txt'],
		},
		{
			'label':1,
			'files':['flows_gnews5.txt']
		},
		{
			'label':2,
			'files':['flows_internet5.txt']
		},
		{
			'label':3,
			'files':['flows_twc5.txt']
		},
		{
			'label':4,
			'files':['flows_youtube5.txt']
		}
	]
	test_set = []
	test_labels = []

	# aggregate the test data along with the labels for it
	for data in test_files:
		label = data['label']
		for filepath in data['files']:
			with open(flowbase+filepath, "r") as file:
				string = find_next_flow(file)
				while not (string == -1):
					features = extract_features(parse_flow(string))
					test_set.append(features)
					test_labels.append(label)
					string = find_next_flow(file)
	
	# Ok, we have the sets now. 
	# Do the SVM
	# sklearn.preprocessing.MinMaxScaler
	# clf=svm.SVC(kernel='poly',degree=2,gamma=1,coef0=0,probability=True) # INSANELY SLOW

	# either save, load, or generate the model
	if load and os.path.exists(flpath):
		clf = load_model(flpath)
	else:
		# clf = tree.DecisionTreeClassifier()
		clf = ensemble.RandomForestClassifier(n_estimators=200)
		clf.fit(training_set, training_labels)
		if save:
			save_model(clf, fspath) # save the trained model for next time

	predictions = clf.predict(test_set)

	print("Accuracy: " + str(accuracy_score(test_labels, predictions)))
	print("Predicted >")
	print("Actual \\/")
	print(confusion_matrix(test_labels, predictions, labels=[0,1,2,3,4]))

'''
Save the model to a given file path

Current implementation uses 'pickle' as it can save the model to a string
See: https://scikit-learn.org/stable/modules/model_persistence.html
'''
def save_model(clf, filepath):
	smodel = pickle.dumps(clf)
	# save to file
	with open(filepath, "wb") as file:
		file.write(smodel)
		file.close()

'''
Loads a model from a given filepath. returns the clf
'''
def load_model(filepath):
	with open(filepath, "rb") as file:
		return pickle.loads(file.read()) # read the file to a string and convert to clf

'''
Grabs the features that we want for our data from an array returned by parse_flow

Can't use: IP, MAC, or Payloads
'''
def extract_features(parsed_flow):
	features = []

	features.append(parsed_flow[3])
	features.append(parsed_flow[4])
	# features.append(pared_flow[5]) # protocol: kinda need to convert this to an int, but also don't necessarily need to use it
	features.append(parsed_flow[6])
	features.append(parsed_flow[7])
	features.append(parsed_flow[8])
	features.append(parsed_flow[9])

	return features

'''
Returns the line with the next flow on it. Ignores burst headers and white space
'''
def find_next_flow(file):
	while True:
		line = file.readline()
			
		if line.startswith('<'):
			return line
		elif len(line) == 0:
			return -1

'''
Give this function a line that looks like 
<source ip><dest ip>....<><><><etc....>

returns an array containing strings for the time, ports, protocol
and integers for the ports, byte counts, and packet counts
'''
def parse_flow(line):
	result = re.findall('<([^>]*)>', line)
	# typecast the appropriate fields
	result[3] = int(result[3])
	result[4] = int(result[4])
	result[6] = int(result[6])
	result[7] = int(result[7])
	result[8] = int(result[8])
	result[9] = int(result[9])

	return result



if __name__=="__main__":
	main()