#!/usr/bin/python
# -*- coding: utf-8 -*-

__VERSION__ = '0.1'
__AUTHOR__ = 'Galkan'
__DATE__ = '22.10.2013'


try:
	import sys
	import os
	import argparse
except ImportError,e:
        import sys
        sys.stdout.write("%s\n" %e)
        sys.exit(1)


class Fuzz:

	def __init__(self, spk_directory):
		self.send_tcp_path = "/usr/local/generic_send_tcp"
		self.spk_directory = spk_directory	

		for file in self.send_tcp_path, self.spk_directory:
			if not os.path.exists(file):
				print >> sys.stderr, "%s Doesn't Exists On The System  "% (file)
				sys.exit(2)


	def run_fuzz(self, target, port, start_point):

		if not self.spk_directory.endswith("/"):
                	self.spk_directory = self.spk_directory + "/"

		count = start_point
		for root, dirs, files in os.walk(self.spk_directory):
			if (len(files)-1) < start_point:
				print >> sys.stderr, "Start_Point Must Be Smaller Than File List !!!"
				sys.exit(3)
		
    			for file in files[count:]:
        			if file.endswith('.spk'):
					file_name = self.spk_directory + file
					fuzz_command = "%s %s %s %s 0 0"% (self.send_tcp_path, target, port, file_name)

					print "%d -> %s : Processing"% (count, file)

					proc = os.popen(fuzz_command,"r")
					while 1:
    						line = proc.readline()
    						if not line:
							print "%d -> %s : Ok"% (count, file)
							break

					count = count + 1

##
### Main, go go go ...
##

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Fuzz the vuln app')
	parser.add_argument('-d','--directory', help='Spk Directory', required=True)
	parser.add_argument('-t','--target', help='Target Ip Address', required=True)
	parser.add_argument('-p','--port', help='Port Number', required=True)
	parser.add_argument('-s','--start_point', help='Start Point', required=True)
	args = parser.parse_args()

	fuzz = Fuzz(args.directory)
	file_list = fuzz.run_fuzz(args.target, args.port, int(args.start_point))

