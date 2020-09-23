#!/usr/bin/python

import os
import re
import sys
import time
import json
import urllib3
import argparse
import requests


urllib3.disable_warnings()


class GoPhish(object):

        def __init__(self):

            usage = "Usage: use --help for further information"
            description = "Create GoPhish Users"
            parser = argparse.ArgumentParser(description = description, usage = usage)

            parser.add_argument('--directory', dest = 'directory', action = 'store', help = 'Directory name where gophish users are stored', required = True)
            parser.add_argument('--groupname', dest = 'groupname', action = 'store', help = 'Name where gophish will add it to group name as pretag', required = True)
        
            args = parser.parse_args()
            
            self.__email_dir = args.directory
            self.__group_name = args.groupname

            api_key = "API-KEY"    
            self.__headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36', 'Content-type':'application/json', 'Authorization':api_key}

            self.__api_url  = "https://IP:PORT/api"
    


        def _run(self):

            count = 1

            for filename in os.listdir(self.__email_dir):
                list_file = "{0}/{1}".format(self.__email_dir, filename)
 
                group_name = "{0}-{1}".format(self.__group_name, count)
                group_json = { "name":group_name, "targets":[] }

                for line in open(list_file, "r"):
                    name = line.split(",")[0].strip()
                    surname = line.split(",")[1].strip()
                    email = line.split(",")[2].strip()
                    position = ""

                    data = { "first_name":name, "last_name":surname, "email":email, "position":position }
                    group_json["targets"].append(data)

                count = count + 1
                group_resp = requests.post("{0}/groups/".format(self.__api_url), data = json.dumps(group_json), headers = self.__headers, verify=False)
                
                print group_name, group_resp

##
### Main
##

if __name__ == "__main__":
    
    gophish = GoPhish()
    gophish._run()

