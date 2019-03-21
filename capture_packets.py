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
import time

def main():
	FILTER = "ip" # TODO: gonna wanna change this

	# TODO: thread this, and then run another thread to print flows
	# Does the ^above^ comment make sense to do?
	sniff(filter=FILTER, prn=handle_sniffed, count=0) # count = 0 means run indefinitely


'''
flows is an object that will keep track of the traffic a flow has received
once a second has passed without traffic, the flow should be logged
keys will be source_ip+","+dest_ip+","+source_port+","+dest_port+","+proto

(keys are for convenience, but don't provide any efficiency)
'''
flows = [] # its an array because we may have repeats in keys
# TODO: Need a lock for the flows object


''' handle_sniffed:
A function that sniff() from scapy will call each time it sniffs a packet

Think of it as the master function that will handle captured traffic

param: packet - the packet that was captured
'''
def handle_sniffed(packet):
	# FYI:
	# subscripting packets is to access specific layers, like TCP or IP. These must be imported from scapy.all
	# to get specific elements reference https://blogs.sans.org/pen-testing/files/2016/04/ScapyCheatSheet_v0.2.pdf
	put_in_flow(packet)
	
'''
Puts a packet into its appropriate flow

This will also maintain the flow structure.

flows [
	{
		'key':'...'
		... info (packet count, etc)

	},...
]
'''
def put_in_flow(packet): # TODO
	if not packet.haslayer(TCP):
		return 
	
	ct = time.time_ns()
	delim = ","
	key = str(packet[IP].src) + delim + str(packet[IP].dst) + delim + str(packet[TCP].sport) + delim + str(packet[TCP].dport) + delim + str(packet[IP].proto)

	# TODO: Grab the lock for the flows

	for flow in flows:
		if flow['key'] == key:
			# found it!
			
			# check timestamp, if its still less than a second update info, otherwise continue on
			if not ct - flow['timestamp'] > 1000000000: # 1e^9
				# TODO: update the info
				return
		
	# it wasn't in the list of flows?
	newflow = {
		'key':key, # for convenience
		'timestamp':time.time_ns()
		# ... the rest of the info
	}
	flows.append(newflow)
	# TODO: Release the lock for the flows
		
'''
Logs a flow

Logging format
<timestamp> <srcaddr> <dstaddr> <srcport> <dstport> <proto> \ <#packets sent> <#packets rcvd> <#bytes send> <#bytes rcvd>
'''
def log_flow(flow):
	# at this point, we assume the lock for the entire list has been grabbed, so we don't need to worry
	print("logged flow") # TODO

'''
General function to call in order to log all the flows that need to be logged.

Note that this won't log any flows that haven't expired yet (>1s)

This is to be called by the thread that logs flows
'''
def log_flows():
	# TODO: Grab the lock for the flows
	ct = time.time_ns()
	for flow in flows:
		if ct - flow['timestamp'] > 1000000000: # 1e^9
			log_flow(flow)

	# update flows to be any flow that hasn't been logged
	flows = [flow for flow in flows if not ct - flow['timestamp'] > 1000000000]
	# TODO: release the lock for the flows

# # make sure to log flows on exit (no longer think this is necessary, but will leave for now)
# def onexit():
# 	for flow in flows:
# 		log_flow(flow)

# import atexit
# atexit.register(onexit)

# run main
if __name__ == '__main__':
	main()
