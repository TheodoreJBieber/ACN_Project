'''
Python class defining a flow.
A flow is a substructure within a packet burst.
A flow is defined by the source ip, destination ip, source port, destination port, and protocol on which the packets are being sent

A flow will contain information such as bytes sent, received, 
'''

from scapy.all import IP, TCP

class Flow:

    def __init__(self, source_ip=None, dest_ip=None, source_port=None, dest_port=None, protocol=None):
        self.source_ip = source_ip
        self.dest_ip = dest_ip
        self.source_port = source_port
        self.dest_port = dest_port
        self.protocol = protocol
        self.packets = []
        self.timestamp = None

    def init(self, source_ip=None, dest_ip=None, source_port=None, dest_port=None, protocol=None):
        self.source_ip = source_ip
        self.dest_ip = dest_ip
        self.source_port = source_port
        self.dest_port = dest_port
        self.protocol = protocol
        self.timestamp = None

    '''
    Syntax: flowObject == packet
    returns: -true if the packet has the same source ip, dest ip, source port, dest port, and protocol as the flow
             -false otherwise
    '''
    def __eq__(self, packet): # TODO: This may change depending on whether the order matters for source/dest
        return (self.source_ip == packet[IP].src and
            self.dest_ip == packet[IP].dst and
            self.source_port == packet[0].sport and
            self.dest_port == packet[0].dport and
            self.protocol == packet[IP].proto)

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
        self.packets.append(packet)
        self.timestamp = packet.time

        return self # return the flow object for convenience
        
    '''
    Prints the current flow summary information
    '''
    def __str__(self): #                                                                                                                                              remove this (below) when done
        return "<timestamp>"+"<"+str(self.source_ip)+">"+"<"+str(self.dest_ip)+">"+"<"+str(self.source_port)+">"+"<"+str(self.dest_port)+">"+"<"+str(self.protocol)+">"+ (str(len(self.packets))) +  "\\"+"<#packets sent> <#packets rcvd> <#bytes send> <#bytes rcvd>"
