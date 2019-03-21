'''
Description:
	A python script that will capture network packets 
	running through this machine.

	This is the first part of a program that will classify
	network traffic.

	Written for Advanced Computer Networks at WPI, 2019 D Term
	Professor Lorenzo De Carli.
Authors: 
	Theodore Bieber
	Thomas White
'''
# installs: libpcap, scapy
from scapy.all import sniff


sniff(filter="ip", prn=handle_sniffed, count=0)


''' handle_sniffed:
A function that sniff() from scapy will call each time it sniffs a packet

Think of it as the master function that will handle captured traffic

param: packet - the packet that was captured
'''
def handle_sniffed(packet):
	print(packet)




# Logging format
# <timestamp> <srcaddr> <dstaddr> <srcport> <dstport> <proto>
#... <#packets sent> <#packets rcvd> <#bytes send> <#bytes rcvd>