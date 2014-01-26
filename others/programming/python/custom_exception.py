#!/usr/bin/python

import sys

class Deneme(Exception):
        def __init__(self, hata_mess):
                self.hata = hata_mess

        def __str__(self):
                return self.hata


def foo():
	if int(sys.argv[1]) > 5:
		raise Deneme("HATA")
	else:
		print "OK"


if __name__ == "__main__":
	try:
		foo()
	except Deneme, mess:
		print mess
 
