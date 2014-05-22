#!/usr/bin/python

"""
In order to install paramiko, follow steps below... 
# apt-get install pip
# pip install ecsda
# wget https://github.com/paramiko/paramiko/archive/master.zip
# unzip master.zip
# python setup.py install
"""

try:
	import paramiko 
	import argparse
	import sys
	import os
	import threading
	import Queue
	import time
except ImportError,e:
        import sys
        sys.stdout.write("%s\n" %e)
        sys.exit(1)



class SshClient:
    TIMEOUT = 5

    def __init__(self, host, port, username, password, passphrase = None):
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.client.connect(host, port, username = username, password = password, timeout = self.TIMEOUT)


    def execute(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)
	return {'out': stdout.readlines(), 'err': stderr.readlines(), 'retval': stdout.channel.recv_exit_status()}

	
    def close(self):
        if self.client is not None:
            self.client.close()
            self.client = None


class Main:
	def __init__(self):

		description = "Kullanim Parametreleri"
        	usage = "Usage: use --help for futher information"
        	parser = argparse.ArgumentParser(description = description, usage = usage)
        	parser.add_argument('-c','--config', dest = 'config', help = 'Configuration File', required = True)
        	parser.add_argument('-t','--thread', dest = 'thread', help = 'Thread Number', required = False)
        	self.args = parser.parse_args()

        	if not os.path.exists(self.args.config):
                	print >> sys.stderr, "%s Doesn't Exists"% (self.args.config)
                	sys.exit(1)

		self.queue_full = True


	def execute_command(self, queue):
	
		while self.queue_full:
                        try:
                                cred_line = queue.get(False)
				ip_addr = cred_line.split(":")[0]
				user = cred_line.split(":")[1]
				passwd = cred_line.split(":")[2]
				command = cred_line.split(":")[3].split(";")

				try:
					client = SshClient(host = ip_addr, port = 22, username = user, password = passwd)
				except Exception, err:
					print >> sys.stderr, "%s : %s"% (ip_addr, str(err))
					sys.exit(1)

				try:
					for cmd in command:
						ret = client.execute(cmd)
						if ret["retval"] == 0:
							print "SUCCCESS: %s - %s : %d\n"% (ip_addr, cmd[:-1], ret["retval"])
							for line in ret["out"]:
								print line[:-1]
						else:
							print "FAIL: %s - %s : %d\n"% (ip_addr, cmd[:-1], ret["retval"])
				finally:
					client.close()		
			
                        except Queue.Empty:
                                self.queue_full = False
			

	def run(self):

		q = Queue.Queue()
		for line in open(self.args.config,"r"):
			if line[0] == "#":
				continue
			else:
				q.put(line)

		if self.args.thread is None:
			self.args.thread = 1

		for i in range(int(self.args.thread)):
			t = threading.Thread(target = self.execute_command, args = (q,))
			t.start()


##
### Main
##

if __name__ == "__main__":
	
	main = Main()
	main.run()
