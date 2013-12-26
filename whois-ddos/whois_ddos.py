#!/usr/bin/python
# -*- coding: utf-8 -*-

__VERSION__ = '0.1'
__AUTHOR__ = 'Galkan'
__DATE__ = '22.09.2013'


try:
  import sys
  import socket
  import optparse
  from Queue import Queue
  from threading import Thread
  import time
  import signal
except ImportError,e:
  import sys
  sys.stdout.write("%s" %e)
  sys.exit(1)


socket.setdefaulttimeout(3)

class NICClient(object) :
    """
	Derivered from http://code.activestate.com/recipes/577364-whois-client/
    """
	
    ABUSEHOST           = "whois.abuse.net"
    NICHOST             = "whois.crsnic.net"
    INICHOST            = "whois.networksolutions.com"
    DNICHOST            = "whois.nic.mil"
    GNICHOST            = "whois.nic.gov"
    ANICHOST            = "whois.arin.net"
    LNICHOST            = "whois.lacnic.net"
    RNICHOST            = "whois.ripe.net"
    PNICHOST            = "whois.apnic.net"
    MNICHOST            = "whois.ra.net"
    QNICHOST_TAIL       = ".whois-servers.net"
    SNICHOST            = "whois.6bone.net"
    BNICHOST            = "whois.registro.br"
    NORIDHOST           = "whois.norid.no"
    IANAHOST            = "whois.iana.org"
    GERMNICHOST         = "de.whois-servers.net"
    DEFAULT_PORT        = "nicname"
    WHOIS_SERVER_ID     = "Whois Server:"
    WHOIS_ORG_SERVER_ID = "Registrant Street1:Whois Server:"


    WHOIS_RECURSE       = 0x01
    WHOIS_QUICK         = 0x02

    ip_whois = [ LNICHOST, RNICHOST, PNICHOST, BNICHOST ]

    def __init__(self) :
        self.use_qnichost = False

        
    def findwhois_server(self, buf, hostname):
        nhost = None
        parts_index = 1
        start = buf.find(NICClient.WHOIS_SERVER_ID)
        if (start == -1):
            start = buf.find(NICClient.WHOIS_ORG_SERVER_ID)
            parts_index = 2
        
        if (start > -1):   
            end = buf[start:].find('\n')
            whois_line = buf[start:end+start]
            whois_parts = whois_line.split(':')
            nhost = whois_parts[parts_index].strip()
        elif (hostname == NICClient.ANICHOST):
            for nichost in NICClient.ip_whois:
                if (buf.find(nichost) != -1):
                    nhost = nichost
                    break
        return nhost
     
   
    def whois(self, query, hostname, flags):
        #pdb.set_trace()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#s.settimeout(3)

        s.connect((hostname, 43))
        if (hostname == NICClient.GERMNICHOST):
            s.send("-T dn,ace -C US-ASCII " + query + "\r\n")
        else:
            s.send(query + "\r\n")
        response = ''
        while True:
	    try:		    	
           	 d = s.recv(4096)
	    except:
		time.sleep(1)
		d = ""
 	
            response += d
            if not d:
                break
        s.close()
        #pdb.set_trace()
        nhost = None
        if (flags & NICClient.WHOIS_RECURSE and nhost == None):
            nhost = self.findwhois_server(response, hostname)
        if (nhost != None):
            response += self.whois(query, nhost, 0)
        return response
    

    def choose_server(self, domain):
        if (domain.endswith("-NORID")):
            return NICClient.NORIDHOST
        pos = domain.rfind('.')
        if (pos == -1):
            return None
        tld = domain[pos+1:]
        if (tld[0].isdigit()):
            return NICClient.ANICHOST
    
        return tld + NICClient.QNICHOST_TAIL
    
    def whois_lookup(self, options, query_arg, flags):
        nichost = None
        #pdb.set_trace()
        # this would be the case when this function is called by other then main
        if (options == None):                     
            options = {}
     
        if ( (not options.has_key('whoishost') or options['whoishost'] == None)
            and (not options.has_key('country') or options['country'] == None)):
            self.use_qnichost = True
            options['whoishost'] = NICClient.NICHOST
            if ( not (flags & NICClient.WHOIS_QUICK)):
                flags |= NICClient.WHOIS_RECURSE
            
        if (options.has_key('country') and options['country'] != None):
            result = self.whois(query_arg, options['country'] + NICClient.QNICHOST_TAIL, flags)
        elif (self.use_qnichost):
            nichost = self.choose_server(query_arg)
            if (nichost != None):
                result = self.whois(query_arg, nichost, flags)           
        else:
            result = self.whois(query_arg, options['whoishost'], flags)
            
        return result
    

def parse_command_line(argv):
    flags = 0
    
    usage = "usage: %prog [options] name"
            
    parser = optparse.OptionParser(add_help_option=False, usage=usage)
    parser.add_option("-a", "--arin", action="store_const", 
                      const=NICClient.ANICHOST, dest="whoishost",
                      help="Lookup using host " + NICClient.ANICHOST)
    parser.add_option("-A", "--apnic", action="store_const", 
                      const=NICClient.PNICHOST, dest="whoishost",
                      help="Lookup using host " + NICClient.PNICHOST)
    parser.add_option("-b", "--abuse", action="store_const", 
                      const=NICClient.ABUSEHOST, dest="whoishost",
                      help="Lookup using host " + NICClient.ABUSEHOST)
    parser.add_option("-c", "--country", action="store", 
                      type="string", dest="country",
                      help="Lookup using country-specific NIC")
    parser.add_option("-d", "--mil", action="store_const", 
                      const=NICClient.DNICHOST, dest="whoishost",
                      help="Lookup using host " + NICClient.DNICHOST)
    parser.add_option("-g", "--gov", action="store_const", 
                      const=NICClient.GNICHOST, dest="whoishost",
                      help="Lookup using host " + NICClient.GNICHOST)
    parser.add_option("-h", "--host", action="store", 
                      type="string", dest="whoishost",
                       help="Lookup using specified whois host")
    parser.add_option("-i", "--nws", action="store_const", 
                      const=NICClient.INICHOST, dest="whoishost",
                      help="Lookup using host " + NICClient.INICHOST)
    parser.add_option("-I", "--iana", action="store_const", 
                      const=NICClient.IANAHOST, dest="whoishost",
                      help="Lookup using host " + NICClient.IANAHOST)
    parser.add_option("-l", "--lcanic", action="store_const", 
                      const=NICClient.LNICHOST, dest="whoishost",
                      help="Lookup using host " + NICClient.LNICHOST)
    parser.add_option("-m", "--ra", action="store_const", 
                      const=NICClient.MNICHOST, dest="whoishost",
                      help="Lookup using host " + NICClient.MNICHOST)
    parser.add_option("-p", "--port", action="store", 
                      type="int", dest="port",
                      help="Lookup using specified tcp port")
    parser.add_option("-Q", "--quick", action="store_true", 
                     dest="b_quicklookup", 
                     help="Perform quick lookup")
    parser.add_option("-r", "--ripe", action="store_const", 
                      const=NICClient.RNICHOST, dest="whoishost",
                      help="Lookup using host " + NICClient.RNICHOST)
    parser.add_option("-R", "--ru", action="store_const", 
                      const="ru", dest="country",
                      help="Lookup Russian NIC")
    parser.add_option("-6", "--6bone", action="store_const", 
                      const=NICClient.SNICHOST, dest="whoishost",
                      help="Lookup using host " + NICClient.SNICHOST)
    parser.add_option("-?", "--help", action="help")

        
    return parser.parse_args(argv)

 

class Worker(Thread):
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()

            try:
                func(*args, **kargs)
            except Exception, e:
                 print e

            self.tasks.task_done()



class ThreadPool():
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): Worker(self.tasks)


    def add_task(self, func, *args, **kargs):
        """Add a task to the queue"""
        self.tasks.put((func, args, kargs))


    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()

 
def signal_handler(signal, frame):
        print 'Ctrl+C ...'
        sys.exit(0)


if __name__ == "__main__":
    	flags = 0
    	nic_client = NICClient()

    	(options, args) = parse_command_line(sys.argv)

    	if (options.b_quicklookup is True):
        	flags = flags|NICClient.WHOIS_QUICK
	
	domain_name = args[1]
	thread_count = args[2]

	while True:
	  	  signal.signal(signal.SIGINT, signal_handler)

		  pool = ThreadPool(int(thread_count))

		  for i in range(int(thread_count)):
			    pool.add_task(nic_client.whois_lookup, options.__dict__,domain_name,flags)		
			    print "%d : thread is started ..."% i

		  pool.wait_completion()



