#!/usr/bin/python

from random import choice
import urllib2
import sys

def random_useragent(url):

        HEADERS = {
                        'User-Agent': 'Mozilla/5.0',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Encoding': 'gzip, deflate',
                        'Connection': 'close',
                        'DNT': '1'
                }


        UAS = [
                        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11',
                        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:17.0) Gecko/20100101 Firefox/17.0',
                        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17',
                        'Mozilla/5.0 (Linux; U; Android 2.2; fr-fr; Desire_A8181 Build/FRF91) App3leWebKit/53.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
                        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; FunWebProducts; .NET CLR 1.1.4322; PeoplePal 6.2)',
                        'Mozilla/5.0 (Windows NT 5.1; rv:13.0) Gecko/20100101 Firefox/13.0.1',
                        'Opera/9.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.01',
                        'Mozilla/5.0 (Windows NT 5.1; rv:5.0.1) Gecko/20100101 Firefox/5.0.1',
                        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 3.5.30729)'
                ]

        request = urllib2.Request(url)
        HEADERS['User-Agent'] = choice(UAS)
        request.add_header('User-Agent', HEADERS)

        response = urllib2.urlopen(request)
        html = response.readlines()

        return html


if __name__ == "__main__":
        url = sys.argv[1]
        result = random_useragent(url)
        print result
        
# Calistirmak icin komut satirindan istenilen url adresinin verilmesi yeterli olmaktadir.

# ./random-useragent http://www.google.com/

