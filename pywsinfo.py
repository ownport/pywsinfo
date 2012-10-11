#!/usr/bin/env python
#
#   Website info gathering
#

# TODO collect WHOIS informatio
# TODO extract meta information from homepage (head, meta)
# TODO add sitemap.xml support
# TODO add choice to select different report types about website
# TODO add choice to select different report format (text, json, html) about website

__author__  = 'Andrey Usov <https://github.com/ownport/pywsinfo>'
__version__ = '0.1'

import socket
import pprint
import requests
import urlparse

# default setting for python-requests
REQUESTS_DEFAULTS = {}

def parse_url(url):  
    ''' parse website url, remove path if exists '''
    url_parts = urlparse.urlparse(url)
    return {
            'source_url': urlparse.urlunsplit((url_parts.scheme,url_parts.netloc,'','','')),
            'host': url_parts.netloc
    }

def nslookup(host):
    ''' returns result of DNS lookup '''
    # return socket.gethostbyname(host)
    try:
        return socket.gethostbyname_ex(host)[2]
    except:
        return []

class WebsiteInfo(object):
    ''' website information '''    
    
    def __init__(self, website_url):    
        self._url = website_url
        self._homepage_content = None
        self._details = parse_url(self._url)
    
    def _make_request(self, method, url):
        ''' make request to website '''        
        result = dict()
        resp = requests.request(method, url)
        
        result['final_url'] = resp.url
        result['status_code'] = resp.status_code
        if 'server' in resp.headers:
            result['server'] = resp.headers['server']
        if 'powered-by' in resp.headers:
            result['powered-by'] = resp.headers['x-powered-by']

        if resp.content:
            result['content'] = resp.content

        return result
    
    def run(self):
        ''' run website info retrieval '''
        
        # nslookup
        self._details['ip_addreses'] = nslookup(self._details['host'])

        # first request to web site. Try to detect 
        if len(self._details['ip_addreses']) > 0:
            resp = self._make_request('GET', self._details['source_url'])
            for k in resp.keys():
                self._details[k] = resp[k]

        # check robots.txt
        if self._details.get('status_code') == 200:
            robots_url = urlparse.urljoin(self._details['final_url'],'/robots.txt')
            resp = self._make_request('GET', robots_url)
            if 'content' in resp:
                self._details['robots.txt'] = resp['content']
                
    
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


