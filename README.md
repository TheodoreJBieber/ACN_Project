# ACN_Project Phase 3

Requirements:
- Python 3.7

Required packages (in requirements.txt)
- scapy (windows may require version 2.4.0 to work. 2.4.1/2 seem to have issues)
- libpcap
- tcpdump? (I don't think we use this on windows, but on the VM we use it)
- sklearn (For the classifier)


**Running Phase3:**

`python3 pip -r requirements.txt && python3 classifyFlows.py "path/to/pcap/file"`

Files:
    
    - flow.py: A file containing the Flow class, which is used to easily create and add to flows
    
    - burst.py: A file containing the Burst class, which is used to easily create Bursts, which contain Flows. Adding a packet to a burst will automatically sort it into the appropriate flow. Printing a burst prints every flow in it


**phase2**    capture_packets.py: Contains a main function that does phase 2 of the project, as well as a function that operates on a pcap file
    
    classifier.py: Creates a classifier with the training and test data in the flows folder. You do not need to use this as we have already created the classifier.


**phase3**    classifyFlows.py: Phase 3 script. Takes in one argument, a file path, where the pcap file is located. Classifies the Flows in the pcap file and prints them out in flow format + a label. This file depends on all of the above files

    write_packets.py: A helper script that captures a bunch of packets for us to use in testing our phase 3

Trained Classifiers:
1. Decision Tree: classifier.tree

2. Random Forest: classifier.randomforest

Potential Issues:

    - The way we trained our model was by using 5 categories, one for each of the apps. Due to this, it will always predict that the flow is from one of these five apps. 

    - Additionally, we have not yet accounted for noise. Noise is present in the captures for each of out five apps, and therefore it is probable that this is reducing the accuracy of our classifier.
        - We attempted to account for this in another flow, but could not generate enough data to get any meaningful resolution into what was really noise.