'''
Python class defining a packet burst data structure
A packet burst is any stream of packets that are separated by no more than 1 second of time between the packets being sent or received. 
'''

from flow import Flow

class Burst:

    def __init__(self, packet=None):
        self.flows = []
        if packet:
            self.flows.append(Flow().__add__(packet))
            self.timestamp = packet.time
        else:
            self.timestamp = None

    '''
    Syntax: self == packet
    returns: -true if the timestamp is less than a second from the most recent addition, or if there is no flow stored currently
             -false otherwise
    '''
    def __eq__(self, packet):
        if self.timestamp:
            return packet.time - self.timestamp < 1
        else: 
            return True

    '''
    The inverse of __eq__
    Syntax: self != timestamp
    returns: -false 
             -true otherwise
    '''
    def __ne__(self, timestamp):
        return not self == timestamp

    '''
    Syntax: flowObject + packet
    Adds a packet to the flow
    '''
    def __add__(self, packet):
        assert (self == packet), "burst timestamp more than a second before packet timestamp"

        added = False # boolean that tracks whether we added the packet to a flow or not
        # if we added it, then we don't need to do anything
        # if we didn't add it, we want to add the packet to a new flow in the list
        for flow in self.flows:
            if flow == packet:
                flow + packet
                added = True

        if not added:
            self.flows.append(Flow().__add__(packet))
        
        return self # return the burst for convenience


        
    '''
    Prints out all of the flows in the burst
    '''
    def __str__(self): 
        string = ""
        for flow in self.flows:
            string+=str(flow) + "\n"
        return string