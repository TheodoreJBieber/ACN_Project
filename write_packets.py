'''
Just a helper program that will write some captured packets to a file
'''
from scapy.all import *


def main():
	FILTER = "ip" # TODO: gonna wanna change this
	packets = sniff(filter=FILTER, count=5000) # count = 0 means run indefinitely
	wrpcap('sniffed_example.pcap', packets)


if __name__ == "__main__":
	main()