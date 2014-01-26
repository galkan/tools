#!/usr/bin/python

import sys
import time
import thread

def main():
        try:
                try:
                        thread.start_new(foo1, ("foo-1",))
                        thread.start_new(foo2, ("foo-2",))
                except:
                        print "Thread Olusturulamadi !!!"
                        sys.exit(1)

                for count in range(1,6):
                        print "Main Thread: %d"% count
                        time.sleep(1)
        except Exception, err:
                print err


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


############################
# ./thread.py 
Main Thread: 1
foo-2 1
foo-1 1
Main Thread: 2
foo-2 2
foo-1 2
Main Thread: 3
foo-2 3
foo-1 3
Main Thread: 4
Main Thread: 5
