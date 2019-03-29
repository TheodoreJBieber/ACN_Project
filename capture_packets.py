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
import sched, time

# also install npcap https://nmap.org/download.html (latest Npcap release self-install worked for me)
from scapy.all import sniff, IP, TCP

import flow
import burst
import queue # for our packets or bursts

reactor = sched.scheduler(time.time, time.sleep)

def main():
	FILTER = "ip" # TODO: gonna wanna change this

	# TODO: thread this, and then run another thread to print flows
	# Does the ^above^ comment make sense to do?
	reactor.enter(.45, 1, check_for_burst)
	reactor.run()
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
		
		

def check_for_burst():
	"""
	Used by the scheduler `reactor` to see if analysis should start
	Will also restart the scheduler in order to keep a constant loop
	"""
	reactor.enter(.45, 1, check_for_burst)
	reactor.run()
	# Don't process if there is nothing to process
	if len(packet_queue) > 0:
		if time.time() - packet_queue[-1].time > 1:
			analyze_burst(packet_queue[-1])

def analyze_burst(last_packet):
	"""
	Handles putting packets into flows, prints, and then archives the burst
	stops processing when `last_packet` is reached
	"""
	current_pkt = packet_queue.get()
	identified_flows = []

	# Group the packets into flows
	while True:
		for flow in identified_flows:
			if flow == current_pkt:
				flow += current_pkt
				break
		# The else statement will trigger if the break never happens
		else:
			identified_flows.append(flow.Flow(
				current_pkt.source_ip,
				current_pkt.dest_ip,
				current_pkt.source_port,
				current_pkt.dest_port,
			))

		if current_pkt is not last_packet:
			current_pkt = packet_queue.get()
		# We've reached the end of the burst,
		# stop dequing
		else:
			break

	# Print out the statistics (formatted in the Flow)
	for flow in identified_flows:
		print(flow)


# # make sure to log flows on exit (no longer think this is necessary, but will leave for now)
# def onexit():
# 	do something

# import atexit
# atexit.register(onexit)

# run main
if __name__ == '__main__':
	main()
