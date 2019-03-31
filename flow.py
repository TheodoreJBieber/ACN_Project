'''
Python class defining a flow.
A flow is a substructure within a packet burst.
A flow is defined by the source ip, destination ip, source port, destination port, and protocol on which the packets are being sent

A flow will contain information such as bytes sent, received, 
'''

from scapy.all import IP, TCP

class Flow:

    def __init__(self, source_ip=None, dest_ip=None, source_port=None, dest_port=None, protocol=None):
        self.init(source_ip, dest_ip, source_port, dest_port, protocol)

    def init(self, source_ip=None, dest_ip=None, source_port=None, dest_port=None, protocol=None):
        self.source_ip = source_ip
        self.dest_ip = dest_ip
        self.source_port = source_port
        self.dest_port = dest_port
        self.protocol = protocol
        
        # tracking
        self.timestamp = None
        self.packets_sent=0
        self.packets_received=0
        self.bytes_sent=0
        self.bytes_received=0



    '''
    Syntax: flowObject == packet
    returns: -true if the packet has the same source ip, dest ip, source port, dest port, and protocol as the flow
             -false otherwise
    '''
    def __eq__(self, packet): # TODO: This may change depending on whether the order matters for source/dest
        return (
            # check if A was source and B was dest
            ((self.source_ip == packet[IP].src and
            self.dest_ip == packet[IP].dst and
            self.source_port == packet[0].sport and
            self.dest_port == packet[0].dport and
            self.protocol == packet[IP].proto))
            or # vice versa
            ((self.dest_ip == packet[IP].src and
            self.source_ip == packet[IP].dst and
            self.dest_port == packet[0].sport and
            self.source_port == packet[0].dport and
            self.protocol == packet[IP].proto)))

    '''
    The inverse of __eq__
    Syntax: flowObject == packet
    returns: -false if the packet has the same source ip, dest ip, source port, dest port, and protocol as the flow
             -true otherwise
    '''
    def __ne__(self, packet):
        return not self == packet

    '''
    Syntax: flowObject + packet
    Adds a packet to the flow
    '''
    def __add__(self, packet): # TODO: still need to add sent/received stuff
        if self.source_ip == None:
            self.init(packet[IP].src,packet[IP].dst,packet[TCP].sport,packet[TCP].dport,packet[IP].proto)

        flowstring = "<"+str(self.source_ip)+">"+"<"+str(self.dest_ip)+">"+"<"+str(self.source_port)+">"+"<"+str(self.dest_port)+">"+"<"+str(self.protocol)+">"
        packetstring = "<"+str(packet[IP].src)+">"+"<"+str(packet[IP].dst)+">"+"<"+str(packet[TCP].sport)+">"+"<"+str(packet[TCP].dport)+">"+"<"+str(packet[IP].proto)+">"
        assert (self == packet), "flow signature " + flowstring + " differs from packet signature " + packetstring
        
        # all good!
        # tracking
        self.timestamp = packet.time
        sent = self.source_ip == packet[IP].src

        if sent:
            self.packets_sent+=1
            self.bytes_sent+=len(packet)
        else:
            self.packets_received+=1
            self.bytes_received+=len(packet)

        return self # return the flow object for convenience
        
    '''
    Prints the current flow summary information
    '''
    def __str__(self): 
        return ("<"+str(self.timestamp)+">"+"<"+str(self.source_ip)+">"+"<"+str(self.dest_ip)+">"+"<"+str(self.source_port)+">"+"<"+str(self.dest_port)+">"+"<"+str(self.protocol)+">"
                +"\\"+"<"+self.packets_sent+">"+"<"+self.packets_received+">"+"<"+self.bytes_sent+">"+"<"+self.bytes_received+">")
