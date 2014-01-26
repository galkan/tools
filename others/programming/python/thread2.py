#!/usr/bin/python

import sys
import time
from threading import Thread

thread_list = []

def main():
        try:
                try:
			t1 = Thread(target = foo1, args=("foo-1",))
			t1.start()
			t2 = Thread(target = foo1, args=("foo-2",))
			t2.start()
                except:
                        print "Thread Olusturulamadi !!!"
                        sys.exit(1)

		thread_list.append(t1)
		thread_list.append(t2)

		for t in thread_list:
			t.join()

        except Exception, err:
                print err
		sys.exit(2)	

def foo1(str):
        for count in range(1,4):
                print "%s %d"% (str,count)
                time.sleep(1)

 
def foo2(str):
        for count in range(1,4):
                print "%s %d"% (str,count)
                time.sleep(1)

if __name__ == "__main__":
        main()


##########
# ./thread2.py 
foo-1 1
foo-2 1
foo-1 2
foo-2 2
foo-1 3
foo-2 3
