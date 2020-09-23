#!/usr/bin/python

import sys
import time
import json
import urllib3
import requests
import argparse

urllib3.disable_warnings()


class GoPhish(object):

    def __init__(self):

        self.__api_url = "https://IP:PORT/api"

        api_key = "API-KEY"    
        self.__headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36', 'Content-type':'application/json', 'Authorization':api_key}

        usage = "Usage: use --help for further information"
        description = "Delete groups, campaigns"
        parser = argparse.ArgumentParser(description = description, usage = usage)

        action_type = ("group", "campaign")

        parser.add_argument('--action_type', dest = 'action_type', action = 'store', help = 'Action Type', choices = action_type, required = True)
        args = parser.parse_args()

        self.__action_type = args.action_type
        self.__action_func = { "group":self.__delete_groups, "campaign":self.__delete_campaigns }



    def __delete_groups(self):

        resp = requests.get("{0}/groups/".format(self.__api_url), headers = self.__headers, verify=False)
        for response in json.loads(resp.text):
            group_id = response['id']
            
            url = "{0}/groups/{1}".format(self.__api_url, group_id)
            group_del = requests.delete(url, headers = self.__headers, verify=False)

            print "Delete_Group - {0} : {1}".format(group_id, group_del)



    def __delete_campaigns(self):

        resp = requests.get("{0}/campaigns/".format(self.__api_url), headers = self.__headers, verify=False)
        for response in json.loads(resp.text):
            campaign_id = response['id']
            
            url = "{0}/campaigns/{1}".format(self.__api_url, campaign_id)
            campaign_del = requests.delete(url, headers = self.__headers, verify=False)
            
            print "Delete_Campaign - {0} : {1}".format(campaign_id, campaign_del)


    def _run(self):

        self.__action_func[self.__action_type]()


##
### Main
##

if __name__ == "__main__":

    gophish = GoPhish()
    gophish._run()
