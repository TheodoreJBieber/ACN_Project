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

from scapy.all import * # import scapy stuff to read in the pcap file

def main():
    argv = sys.argv
    argc = len(argv)

    if argc > 1:
        pcap_path = argv[1]

    model_path = "classifier.randomforest" # set the default path to the random forest model
    clf = load_model(model_path)

    print(capture_packets.read_from_file(pcap_path))

    # now perform predictions on the flows
    # predictions = clf.predict(test_set)


'''
Loads a model from a given filepath. returns the clf
'''
def load_model(filepath):
	with open(filepath, "rb") as file:
		return pickle.loads(file.read()) # read the file and convert to clf

if __name__=="__main__":
	main()