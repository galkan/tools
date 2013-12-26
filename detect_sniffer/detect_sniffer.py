#!/usr/bin/python
# -*- coding: utf-8 -*-

__VERSION__ = '0.1'
__AUTHOR__ = 'Galkan'
__DATE__ = '22.09.2013'

import sys

try:
    from scapy.all import *
except ImportError:
    sys.stderr.write("Scapy module must be installed in order to run this script !!!\n")
    sys.exit(37)   
   

def usage ():
    sys.stderr.write("%s  <-ip ip_address | -net net> \n"% (sys.argv[0]))
    sys.stderr.write("%s -ip 10.0.0.37 | -net 192.168.1.0/24\n"% (sys.argv[0]))
    sys.exit(37)


def is_net_sniffer(net):
    fake_bcast="ff:ff:ff:ff:ff:fe"
    
    ans,unans = srp(Ether(dst=fake_bcast)/ARP(pdst=net), 
    filter="arp and arp[7] = 2", timeout=1, iface_hint=net) 
    ans = ARPingResult(ans.res, name="bga.com.tr") 
   	 
    for snd,rcv in ans:
        print rcv.sprintf("%ARP.psrc%")

    
def is_ip_sniffer (ip_address):
    fake_bcast="ff:ff:00:00:00:00"

    responses = srp1(Ether(dst=fake_bcast) / ARP(op="who-has", pdst=destination_ip),type=ETH_P_ARP, iface_hint=destination_ip, timeout=1, verbose=0) 

    if responses:
        print "%s :OK"% (ip_address)
    else:
        print "%s: NOT"% (ip_address)

        

if __name__ == "__main__":
    
    
    if len(sys.argv) != 3:
	usage()	
    elif (sys.argv[1] == "-ip" and sys.argv[2]) :
        destination_ip = sys.argv[2]
        is_ip_sniffer(destination_ip)
    elif (sys.argv[1] == "-net" and sys.argv[2]):
        net = sys.argv[2]
        is_net_sniffer(net)
    else:
	usage()
