#!/usr/bin/python

import sys

class CustomExceptions(Exception):
        def __init__(self, err_mess):
                self.err = err_mess

        def __str__(self):
                return self.err


class Deneme:

        def __init__(self):
                try:
                        self.file_path = sys.argv[1]
                except:
                        raise CustomExceptions("Komut satiri argumani alinamadi !!!")

        def foo(self):
                try:
                        for line in open(self.file_path, "r"):
                                print line
                except Exception, err:
                        raise CustomExceptions("%s"% err)



if __name__ == "__main__":

        try:
                deneme = Deneme()
                deneme.foo()
        except CustomExceptions, mess:
                print >> sys.stderr, mess
                sys.exit(1)
