#!/usr/bin/python3

import os
import sys
import string
import random
import argparse


class ParseExcel(object):

    def __init__(self):

        usage = "Usage: use --help for further information"
        description = "Parse Excel File to Create Email List for GoPhish"
        parser = argparse.ArgumentParser(description = description, usage = usage)

        parse_type_action = ("only_email", "name_surname_email")

        parser.add_argument('--file', dest = 'file', action = 'store', help = 'Excel File', required = True)
        parser.add_argument('--parser_type', dest = 'parser_type', action = 'store', help = 'Parser Type', choices = parse_type_action, required = True)

        args = parser.parse_args()
        
        self.__excel_file = args.file
        self.__parser_type = args.parser_type

        if not os.path.exists(self.__excel_file):
            print("File '{0}' Doesn't Exists !!!".format(self.__excel_file))
            sys.exit(1)

        self.__results = []



    def __only_email(self, line):

        splitted_line = line.split(".")

        email = ""
        surname = ""

        _name = splitted_line[0].lower().strip()
        name = "{0}{1}".format(_name[0].upper(), _name[1:]).strip()
        
        _surname = splitted_line[1].split("@")[0].lower().strip()
        surname = "{0}{1}".format(_surname[0].upper(), _surname[1:])
        
        email = line.strip().lower()
 
        result = "{0},{1},{2},".format(name, surname, email)
        self.__results.append(result)



    def __name_surname_email(self, line):

        pass



    def _run(self):

        for line in open(self.__excel_file, "r"):
    
            if not "@" in line:
                print("{0} doesn't contain '@'".format())
            else:
                if self.__parser_type == "only_email":
                    self.__only_email(line)
                else:
                    self.__name_surname_email(line)        


        for count in range(1,10):
            random.shuffle(self.__results)
        
        for email_line in set(self.__results):
            print(email_line)

##
### Main
##

if __name__ == "__main__":
    excel_parser = ParseExcel()
    excel_parser._run()

