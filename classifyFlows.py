'''
Classifies flows from a pcap trace
'''
import sys
import os

from sklearn import tree
from sklearn import ensemble

import pickle

import flow
import capture_packets
import classifier # helper functions to create feature vectors from flow strings

from scapy.all import * # import scapy stuff to read in the pcap file

import tempfile as tp

def main():
    argv = sys.argv
    argc = len(argv)

    if argc > 1:
        pcap_path = argv[1]

    model_path = "classifier.randomforest" # set the default path to the random forest model
    clf = load_model(model_path)

    flowstring = capture_packets.read_from_file(pcap_path)
    tempfile = tp.TemporaryFile(mode='w+')
    tempfile.write(flowstring)
    tempfile.seek(0) # go back to start of file

    fstring = classifier.find_next_flow(tempfile)
    features = []
    print("looping")
    while not (fstring==-1):
        feature = classifier.extract_features(classifier.parse_flow(fstring))
        features.append(feature)
        fstring = classifier.find_next_flow(tempfile)

    preds = clf.predict(features)

    # predictions = clf.predict(test_set)
    print(classifier.map_predictions_to_strings(preds))
    # close
    tempfile.close() # close/get rid of temp file


'''
Loads a model from a given filepath. returns the clf
'''
def load_model(filepath):
	with open(filepath, "rb") as file:
		return pickle.loads(file.read()) # read the file and convert to clf

if __name__=="__main__":
	main()