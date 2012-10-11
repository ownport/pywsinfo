#!/usr/bin/env python
#
#   Website info gathering
#

# TODO collect WHOIS informatio
# TODO extract meta information from homepage (head, meta)
# TODO add robots.txt support
# TODO add sitemap.xml support
# TODO add choice to select different report types about website
# TODO add choice to select different report format (text, json, html) about website

__author__  = 'Andrey Usov <https://github.com/ownport/pywsinfo>'
__version__ = '0.1'

import socket
import pprint
import requests
import urlparse

def parse_url(url):  
    ''' parse website url, remove path if exists '''
    url_parts = urlparse.urlparse(url)
    return {
            'website.url': urlparse.urlunsplit((url_parts.scheme,url_parts.netloc,'','','')),
            'website.host': url_parts.netloc
    }

def nslookup(host):
    ''' returns result of DNS lookup '''
    # return socket.gethostbyname(host)
    return socket.gethostbyname_ex(host)[2]

class WebsiteInfo(object):
    ''' website information '''    
    
    def __init__(self, website_url):    
        self._url = website_url
        self._details = self._parse_url(self._url)
    
    def _make_request(self, method, url):
        pass
    
    def run(self):
        ''' run website info retrieval '''
        self._details['website.ip_addreses'] = self._nslookup(self._details['website.host'])
    
    def report(self):
        ''' website report '''
        
        pprint.pprint(self._details)

if __name__ == '__main__':
    
    import argparse
    parser = argparse.ArgumentParser(description='website info extraction')
    parser.add_argument('-u', '--url', help='website url')
    
    args = parser.parse_args()
    
    if args.url:
        wsinfo_process = WebsiteInfo(args.url)
        wsinfo_process.run()
        wsinfo_process.report()
    else:
        parser.print_help()


