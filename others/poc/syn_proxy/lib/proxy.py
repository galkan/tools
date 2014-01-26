__VERSION__ = '0.1'
__AUTHOR__ = 'Galkan'
__DATE__ = '2014'

try:
	import sys
	import re
	import time
	import socket
	import fcntl
	import struct
	from daemon import Daemon
        import logging
        logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
        from scapy.all import *
except ImportError,e:
        import sys
        sys.stdout.write("%s\n" %e)
        sys.exit(1)


class Syn_Proxy(Daemon):

	def __init__(self, pidfile, interface):
		super(Syn_Proxy, self).__init__(pidfile)
                self.interface = interface


        def is_port_open(self, port, ip_addr):

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                address = ip_addr

                try:
                        s.bind((ip_addr, port))
                        s.close()
                        return 0
                except:
                        s.close()
                        return 1


        def syn_proxy(self, pkt, ip_addr):

                destination_port = pkt[0].dport
                destination_ip = pkt[1].dst

                my_ack = int(pkt[0].seq + 1)
                source_port = pkt[0].sport
                source_ip = pkt[1].src

                port_status = self.is_port_open(destination_port, ip_addr)
                if port_status == 0:
			flags = pkt.sprintf(r"%TCP.flags%")
                        if destination_ip == ip_addr and flags == "S":
                                ip = IP(src = "%s"% destination_ip, dst = "%s"% source_ip)
                                TCP_ACK = TCP(sport = destination_port, dport = source_port, flags = "SA", ack = my_ack)
                                send(ip/TCP_ACK)
				


	def get_ip_addr(self, ifname):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    		return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])



	def run(self):
		ip_addr = self.get_ip_addr(self.interface)
                while True:
                        sniff(store = 0, filter = "tcp", iface = self.interface, prn = lambda pkt: self.syn_proxy(pkt, ip_addr))

