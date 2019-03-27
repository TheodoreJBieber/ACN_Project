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
# pip installs: libpcap, scapy==2.4.0 !!! scapy version > 2.4.0 has unresolved issues on windows
# also could do pip install -r requirements.txt
# also install npcap https://nmap.org/download.html (latest Npcap release self-install worked for me)
from scapy.all import sniff, IP, TCP
import flow
import burst
import queue # for our packets or bursts

def main():
	FILTER = "ip" # TODO: gonna wanna change this

	# TODO: thread this, and then run another thread to print flows
	# Does the ^above^ comment make sense to do?
	sniff(filter=FILTER, prn=handle_sniffed, count=0) # count = 0 means run indefinitely

# queue for storing our packets, Queue is FIFO, we can also do LifoQueue, PriorityQueue, or a SimpleQueue that is a less useful version of Queue
packet_queue = queue.Queue(0) # 0 is the default, indicating that the maximum size is infinite
mylist = []


''' handle_sniffed:
A function that sniff() from scapy will call each time it sniffs a packet

Think of it as the master function that will handle captured traffic

param: packet - the packet that was captured
'''
def handle_sniffed(packet):
	# FYI:
	# subscripting packets is to access specific layers, like TCP or IP. These must be imported from scapy.all
	# to get specific elements reference https://blogs.sans.org/pen-testing/files/2016/04/ScapyCheatSheet_v0.2.pdf
	# put_in_flow(packet)
	if packet.haslayer(TCP) and packet.haslayer(IP): # so this line we will probably need to remove at some point, but we also need the IP and TCP layers in order to get some information with scapy
		packet_queue.put(packet)
		
		


# # make sure to log flows on exit (no longer think this is necessary, but will leave for now)
# def onexit():
# 	do something

# import atexit
# atexit.register(onexit)

# run main
if __name__ == '__main__':
	main()
