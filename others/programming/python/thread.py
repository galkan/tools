#!/usr/bin/python

import sys
import time
import thread

def main():
        try:
                try:
                        thread.start_new(foo1, ("deneme-1",))
                        thread.start_new(foo2, ("deneme-2",))
                except:
                        print "Thread Olusturulamadi !!!"
                        sys.exit(1)

                for count in range(1,5):
                        print count
                        time.sleep(1)
        except Exception, err:
                print err


def foo1(url):
        for count in range(1,10):
                print "Foo-1 %d"% count
                time.sleep(1)

def foo2(url):
        for count in range(1,10):
                print "Foo-2 %d"% count
                time.sleep(1)

 
if __name__ == "__main__":
        main()


---------------------------------
# ./thread.py
1
 Foo-2 1
Foo-1 1
2
 Foo-1 2
Foo-2 2
Foo-1 3
 Foo-2 3
3
Foo-2 4
Foo-1 4
 4
Foo-2 5

