#!/usr/bin/python


__VERSION__ = '0.1'
__AUTHOR__ = 'Galkan'
__DATE__ = '01..2014'


try:
	import sys
	import re
	import os
	import argparse
	import syslog
	import subprocess
	import logging
	logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
        from scapy.all import *
	from lib.daemon import Daemon
	from lib.common import *
except ImportError,e:
        import sys
        sys.stdout.write("%s\n" %e)
        sys.exit(1)


class SSH(Daemon):

	def __init__(self, pidfile, whitelist_file, interface):

                if not os.path.exists(tcpkill_path):
			print >> sys.stderr, "%s -> Dosyasi Sistemde Bulunamadi. Dniff yazilimini sisteme yukleyin. !!!"% tcpkill_path
			sys.exit(2)

		if not os.path.exists(whitelist_file):
			print >> sys.stderr, "%s -> Dosyasi Sistemde Bulunamadi !!!"% whitelist_file
			sys.exit(3)

		super(SSH, self).__init__(pidfile)
        	self.ssh_reg = re.compile("SSH\-[12]\.[0-9]", re.IGNORECASE)
		self.whitelist = open(whitelist_file,"r").readlines()
		self.interface = interface


	def logging (self,log_message):
		syslog.openlog("SSH-Block",0,syslog.LOG_LOCAL3)
		syslog.syslog("%s" % log_message)
		syslog.closelog()


	def killConnection (self, src, src_port, dst, dst_port):
		kill_command  = "%s -i %s src host %s and dst host %s and dst port %d &"% (tcpkill_path, self.interface, dst, src, src_port)
		proc = subprocess.Popen([kill_command],shell=True,stdout=subprocess.PIPE,)
                stdout_value = str(proc.communicate())


	def main(self, packet):
		src = packet.sprintf("%IP.src%")
        	dst = packet.sprintf("%IP.dst%")

                payload = packet.sprintf("%Raw.load%")
                if re.search(self.ssh_reg, payload):
			src_port = packet[TCP].sport
			dst_port = packet[TCP].dport

			is_whitelisted = 0
			for line in self.whitelist:
				ip = line.split("\n")[0]
				if src == ip:
					is_whitelisted = 1	

			if not is_whitelisted == 1:
				self.logging("%s -> %s:%s"% (src, dst, dst_port))
				self.killConnection(src, src_port, dst, dst_port)


	def run (self):
		while True:
			sniff(store = 0, filter = "tcp", iface = self.interface, prn = lambda pkt: self.main(pkt))


##
### Go Galkan go go go ...
##


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
        parser.add_argument('--iface', '-i', action = 'store', dest = 'iface', required = True)
        parser.add_argument('--command', '-c', action = 'store', dest = 'command', choices=('start', 'stop'), required = True)
        parser.add_argument('--whitelist', '-w', action = 'store', dest = 'whitelist', required = True)
        args = parser.parse_args()
 
        daemon  = SSH(ssh_block_pid, args.whitelist, args.iface)
        if args.command == "start":
        	daemon.start()
	else:
                daemon.stop()
