#!/usr/bin/python

import sys
import time
import json
import urllib3
import requests


urllib3.disable_warnings()


class GoPhish(object):


    def __init__(self):

        self.__api_url  = "https://IP:PORT/api"
    
        api_key = "API-KEY"
        self.__headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36', 'Content-type':'application/json', 'Authorization':api_key}



    def _run(self):

        count = 1

        resp = requests.get("{0}/groups/".format(self.__api_url), headers = self.__headers, verify=False)
        for response in json.loads(resp.text):
            group_name = response['name']

            campaign_data = {
                    "name": "Campaign-Name - {0}".format(count),
                    "template": { "name": "Template-Name" },
                    "page": { "name": "Page-Name" },
                    "smtp": { "name": "Smtp-Name" },
                    "url": "http://URL/ - {{.URL}}",
                    "groups": [{"name": "{0}".format(group_name),}]
                }
        
            print "Campaign : '{0}' - {1}".format(group_name, count)    
            
            campaign_resp = requests.post("{0}/campaigns/".format(self.__api_url), data = json.dumps(campaign_data), headers = self.__headers, verify=False)
            count = count + 1

            #time.sleep(60)

##
### Main
##

if __name__ == "__main__":
    gophish = GoPhish()
    gophish._run()
