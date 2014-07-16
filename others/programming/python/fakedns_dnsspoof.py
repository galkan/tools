#!/usr/bin/env python

try:
	import sys
	import argparse
	import socket
	import re
except ImportError,e:
        import sys
        sys.stdout.write("%s\n" %e)
        sys.exit(1)
	
"""
it is derived from http://code.activestate.com/recipes/491264-mini-fake-dns-server/
"""

class DnsSpoof:

  	def __init__(self):

		parser = argparse.ArgumentParser()
                parser.add_argument('--file', '-f', action = 'store', dest = 'file', help = "DNS Files", metavar="FILE", required = True)
                args = parser.parse_args()

                try:
                        self.db_file = open(args.file,"r")
                        self.domain_list = self.db_file.readlines()
                except Exception, err:
                        print >> sys.stderr, str(err)
                        sys.exit(1)


	def init_data(self, data):
	
    		self.data = data
    		self.dominio = ''

    		tipo = (ord(data[2]) >> 3) & 15   # Opcode bits
    		if tipo == 0:                     # Standard query
      			ini = 12
      		lon = ord(data[ini])
      		while lon != 0:
        		self.dominio += data[ini+1:ini+lon+1] + '.'
        		ini += lon+1
        		lon = ord(data[ini])
			


 	def response(self, ip):

    		packet = ''
    		if self.dominio:
      			packet += self.data[:2] + "\x81\x80"
      			packet += self.data[4:6] + self.data[4:6] + '\x00\x00\x00\x00'   
      			packet += self.data[12:]                                         
      			packet += '\xc0\x0c'                                             
      			packet += '\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'             
      			packet += str.join('',map(lambda x: chr(int(x)), ip.split('.'))) 
    		return packet


	def main(self):

		udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                udps.bind(('',53))

		try:
                        while 1:
                                data, addr = udps.recvfrom(1024)
                                dns_spoof = self.init_data(data)

                                domain = str(data.split('\x00')[8])
                                real_domain = ""
                                dot_index = 0
                                while True:
                                        try:
                                                content_dot_index = ord(domain[dot_index])
                                        except:
                                                break

					start = dot_index + 1
                                        stop = dot_index + content_dot_index
                                        real_domain = real_domain + domain[start:stop+1].split("\n")[0] + "."
                                        dot_index = stop + 1

				control = 0
                                for line in self.domain_list:
                                        new_line = line[:-1].split()
                                        if re.search("^%s$"% real_domain[:-1],new_line[1]):
                                                control = 1
                                                break
					elif re.search("\*\.", new_line[1]):
                                                if re.search("%s$"%new_line[1].split("*")[1], real_domain[:-1]):
                                                        control = 1
                                                        break

                                if control == 1:
                                        udps.sendto(self.response(line.split()[0]), addr)
                                else:
                                	try:	
                                        	response_ip = socket.gethostbyname(real_domain[:-1])
                                        	udps.sendto(self.response(response_ip), addr)
					except:
						pass

                except KeyboardInterrupt:
                        self.db_file.close()
                        udps.close()

##
### Main
##
					
if __name__ == '__main__':
  	
		dns_spoof = DnsSpoof()
		dns_spoof.main()
