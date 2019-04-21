import sys

from sklearn import ensemble, tree

import capture_packets
import classifier # helper functions to create feature vectors from flow strings
from classifyFlows import load_model
import flow


def main():
    """
    Label flows on the fly. Assumes that input is:
      - Coming from stdin
      - Coming from capture_packets.py (or is similarly formated)
    Will loop infinitely, must be stopped by KeyboardInterrupt
    """
    # Python treats sys.std* like a File
    flow_input = sys.stdin

    clf = load_model('classifier.randomforest.linux')

    # Track number of bursts to match desired output
    burst_counter = 0

    # Just in case there are empty spaces or junk data,
    # seek to the line that is the start of a burst
    find_start_of_burst(flow_input)
    current_flows = []
    flow_features = []
    while True:
        # We know that our assumed input has no spaces
        # between flows when inside a burst, so it is
        # safe to assume that readline() will return a flow
        raw_flow = flow_input.readline()
        if "END OF BURST" not in raw_flow:
            current_flows.append(raw_flow)
            flow_features.append(classifier.extract_features(classifier.parse_flow(raw_flow)))
        else:
            # attempt to label the flows
            preds = clf.predict(flow_features)
            labels = classifier.map_predictions_to_strings(preds)

            # handle outputing the flow information
            burst_counter += 1
            print("\nBurst {}:".format(burst_counter))
            # `zip()` returns an iterable in O(1)
            for flow, label in zip(current_flows, labels):
                print(flow.strip("\n") + " <" +label+">")

            # Reset the tracking variables
            current_flows = []
            flow_features = []
            find_start_of_burst(flow_input)


def find_start_of_burst(f):
    """
    Seaches for the ===START OF BURST===
    """
    while True:
        line = f.readline()

        if "START OF BURST" in line:
            return line


if __name__ == "__main__":
    main()