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

def main():
	FILTER = "ip proto tcp or ip6 proto tcp" # captures tcp over ipv4 and ipv6. Maybe change?

	# optionally, we could thread this part, and may even want to at some point
	sniff(filter=FILTER, prn=handle_sniffed, count=0) # count = 0 means run indefinitely


# flows is an object that will keep track of the traffic a flow has received
# once a second has passed without traffic, the flow should be logged
# keys will be source_ip+","+dest_ip+","+source_port+","+dest_port+","+proto
flows = []

''' handle_sniffed:
A function that sniff() from scapy will call each time it sniffs a packet

Think of it as the master function that will handle captured traffic

param: packet - the packet that was captured
'''
def handle_sniffed(packet):
	# FYI:
	# subscripting packets is to access specific layers, like TCP or IP. These must be imported from scapy.all
	# to get specific elements reference https://blogs.sans.org/pen-testing/files/2016/04/ScapyCheatSheet_v0.2.pdf
	print("got a packet!")
	



# Logging format
# <timestamp> <srcaddr> <dstaddr> <srcport> <dstport> <proto>
#... <#packets sent> <#packets rcvd> <#bytes send> <#bytes rcvd>
def log_flow(flow):
	# So, I started off somewhat poorly here
	# We want to count the number of packets sent and received within a flow
	# currently, this won't do it

	# probably need to change var names, but the code is still useful
	# if(packet.haslayer(TCP)): # not all of these use tcp, so for now just don't print anything
	# 	delim = " "
	# 	logged = ""
	# 	logged += "<timestamp>" + delim
	# 	logged += str(packet[IP].src) + delim
	# 	logged += str(packet[IP].dst) + delim
	# 	logged += str(packet[TCP].sport) + delim
	# 	logged += str(packet[TCP].dport) + delim
	# 	logged += str(packet[IP].proto) + delim + "\\"
	# 	logged += "<#packets sent>" + delim
	# 	logged += "<#packets rcvd>" + delim
	# 	logged += "<#bytes send>" + delim
	# 	logged += "<#bytes rcvd>" + delim
	# else:
	# 	return

	print("logged flow")


# make sure to log flows on exit
def onexit():
	for flow in flows:
		log_flow(flow)

import atexit
atexit.register(onexit)

# run main
if __name__ == '__main__':
	main()
