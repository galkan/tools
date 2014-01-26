#!/usr/bin/python

__VERSION__ = '0.1'
__AUTHOR__ = 'Galkan'
__DATE__ = '2014'

try:
	import sys
	import argparse
	from lib.proxy import Syn_Proxy
except ImportError,e:
        import sys
        sys.stdout.write("%s\n" %e)
        sys.exit(1)


class Main:
	def __init__(self):
		self.pid = "/var/run/syn_proxy.pid"

	def run(self):
		parser = argparse.ArgumentParser()
		parser.add_argument('--iface', '-i', action = 'store', dest = 'iface', required = True)
		parser.add_argument('--command', '-c', action = 'store', dest = 'command', choices=('start', 'stop'), required = True)
		args = parser.parse_args()
		

		daemon  = Syn_Proxy(self.pid, args.iface)
		if args.command == "start":
			daemon.start()
		elif args.command == "stop":
			daemon.stop()

##
### Galkan, go go go ...
##

if __name__ == "__main__":
	main = Main()
	main.run()
