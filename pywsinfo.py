#!/usr/bin/env python
#
#   Website info gathering
#

# TODO collect WHOIS information
# TODO extract meta information from homepage (head, meta)
# TODO add sitemap.xml support
# TODO add choice to select different report types about website
# TODO add choice to select different report format (text, json, html) about website
# TODO read robots.txt from string

__author__  = 'Andrey Usov <https://github.com/ownport/pywsinfo>'
__version__ = '0.1'

import re
import socket
import pprint
import requests
import urlparse
import datetime

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

    def _handle_html_head(self, content):
        ''' handle HTML head, extract keywords & description '''
        
        result = dict()
        
        content = content.replace('\r', '')
        content = content.replace('\n', '')
        head = ''.join(re.findall(r'<head>(.+?)</head>', content, re.I))
        metas = re.findall(r'<meta(.+?)[\/]?>', head, re.I)
        for meta in metas:
            meta_dict = dict(re.findall(r'(\w+)\s*=\s*"(.+?)"', meta, re.I))
            if 'name' in meta_dict:
                if meta_dict['name'].lower() == 'keywords':
                    result['keywords'] = [c.strip() for c in meta_dict['content'].split(',')]
                if meta_dict['name'].lower() == 'description':
                    result['description'] = meta_dict['content']
        return result
    
    def run(self):
        ''' run website info retrieval '''
        
        # nslookup
        self._details['ip_addreses'] = nslookup(self._details['host'])

        # first request to web site. Try to detect 
        if len(self._details['ip_addreses']) > 0:
            resp = self._make_request('GET', self._details['source_url'])
            for k in resp.keys():
                if k == 'content':
                    head_params = self._handle_html_head(resp[k])
                    for k in head_params:
                        self._details[k] = head_params[k]
                else:
                    self._details[k] = resp[k]

        # check robots.txt
        if self._details.get('status_code') == 200:
            robots_url = urlparse.urljoin(self._details['final_url'],'/robots.txt')
            resp = self._make_request('GET', robots_url)
            if resp['status_code'] == 200 and 'content' in resp:
                self._details['robots.txt'] = resp['content']
                # TODO extract link to sitemap.xml
                for line in self._details['robots.txt'].split('\n'):
                    if line.startswith('Sitemap'):
                        if 'sitemaps' not in self._details:
                            self._details['sitemaps'] = list()
                        self._details['sitemaps'].append(line.replace('Sitemap:', '').strip())

        # check default sitemap
        if 'sitemaps' not in self._details:
            sitemaps_url = urlparse.urljoin(self._details['final_url'],'/sitemap.xml')
            resp = self._make_request('HEAD', sitemaps_url) 
            if resp['status_code'] == 200:
                self._details['sitemaps'] = sitemaps_url
            
    
        # latest update datetime
        self._details['last_update'] = str(datetime.datetime.now())
    
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


