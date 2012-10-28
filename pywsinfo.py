#!/usr/bin/env python
#
#   Website info gathering
#

# TODO collect WHOIS information
# TODO add choice to select different report types about website
# TODO add choice to select different report format (text, json, html) about website
# TODO add sitemap-image support (http://support.google.com/webmasters/bin/answer.py?hl=en&answer=178636&topic=20986&ctx=topic)
# TODO add sitemap-vide support ({http://www.google.com/schemas/sitemap-video/1.0}video)

__author__  = 'Andrey Usov <https://github.com/ownport/pywsinfo>'
__version__ = '0.1'

import re
import sys
import socket
import requests
import urlparse
import datetime

from gzip import GzipFile 
from cStringIO import StringIO

try:
    import xml.etree.cElementTree as xml_parser
except ImportError:
    import xml.etree.ElementTree as xml_parser

# default setting for python-requests
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) pywsinfo/{}'.format(__version__)
requests.defaults.defaults['base_headers']['User-Agent'] = USER_AGENT

NAMESPACES = (
    '{http://www.google.com/schemas/sitemap/0.84}',
    '{http://www.google.com/schemas/sitemap/0.9}',
    '{http://www.sitemaps.org/schemas/sitemap/0.9}',
)

def validate_url(url):
    ''' returns True if url validated '''
    pass
 
def parse_url(url):  
    ''' parse website url, remove path if exists '''
    url_parts = urlparse.urlparse(url)
    source_url = urlparse.urlunsplit((url_parts.scheme,url_parts.netloc,'','',''))
    
    if ':' in url_parts.netloc:
        host, port = url_parts.netloc.split(':')
    else:
        host = url_parts.netloc
    return { 'source_url': source_url, 'host': host }

def nslookup(host):
    ''' returns result of DNS lookup '''
    # return socket.gethostbyname(host)
    try:
        return socket.gethostbyname_ex(host)[2]
    except:
        return []

# Entity escape
# 
# Character	            Escape Code
# ---------------------+-----------
# Ampersand(&)	        &amp;
# Single Quote (')      &apos;
# Double Quote (")	    &quot;
# Greater Than (>)	    &gt;
# Less Than	(<)	        &lt;

def parse_html_head(content):
    ''' parse HTML head, extract keywords & description '''
    
    # TODO extract links to RSS/Atom feeds
    # <link rel="alternate" type="application/rss+xml"  href="http://www.example.com/rss.xml" title="Example RSS Feed">
    
    # TODO extract info about generators
    # <meta name="generator" content="WordPress 3.4.2" />
    
    # TODO links to RSS/Atom
    # <link rel="alternate" type="application/rss+xml" title="RSS 2.0" href="..." />
    # <link rel="alternate" type="text/xml" title="RSS .92" href="..." />
    # <link rel="alternate" type="application/atom+xml" title="Atom 0.3" href="..." />
    
    result = dict()
    
    content = content.replace('\r', '')
    content = content.replace('\n', '')
    # select HEAD section
    head = ''.join(re.findall(r'<head(.+?)</head>', content, re.I))
    # extract title information
    title = ''.join(re.findall(r'<title>(.+?)</title>', content, re.I))
    if title:
        result['title'] = title.strip()
    # select meta information: keywords and description
    metas = re.findall(r'<meta(.+?)[/]?>', head, re.I)
    for meta in metas:
        meta_dict = dict(re.findall(r'(\w+)\s*=\s*"(.+?)"', meta, re.I))
        if 'name' in meta_dict and 'content' in meta_dict:
            # keywords
            if meta_dict['name'].lower() == 'keywords':
                result['keywords'] = [c.strip() for c in meta_dict['content'].split(',')]
            # description
            if meta_dict['name'].lower() == 'description':
                result['description'] = meta_dict['content']
    
    return result

# -----------------------------------------------
#   WebsiteInfo
# -----------------------------------------------
class WebsiteInfo(object):
    ''' website information '''    
    
    def __init__(self, website_url, debug=False):    
        self._debug = debug
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

    def _check_robots_txt(self):
        ''' robots.txt '''
        pass

    def _check_sitemap(self):
        ''' sitemap.xml '''
        pass
        
    def gather(self):
        ''' run website info retrieval '''
        
        # nslookup
        self._details['ip_addreses'] = nslookup(self._details['host'])

        # first request to web site. Try to detect 
        if len(self._details['ip_addreses']) == 0:
            raise RuntimeError('Cannot resolve IP addresses for host')
            
        resp = self._make_request('GET', self._details['source_url'])
        for k in resp.keys():
            if k == 'content':
                head_params = parse_html_head(resp[k])
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
                
                # extract link to sitemap.xml
                for line in self._details['robots.txt'].split('\n'):
                    if line.startswith('Sitemap'):
                        if 'sitemaps' not in self._details:
                            self._details['sitemaps'] = list()
                        sitemap_url = line.replace('Sitemap:', '').strip()
                        if not sitemap_url.startswith('http'):
                            sitemap_url = urlparse.urljoin(self._details['final_url'], sitemap_url)
                        self._details['sitemaps'].append(sitemap_url)

        # check default sitemap
        if 'sitemaps' not in self._details:
            sitemaps_url = urlparse.urljoin(self._details['final_url'],'/sitemap.xml')
            resp = self._make_request('HEAD', sitemaps_url) 
            if resp['status_code'] == 200:
                self._details['sitemaps'] = sitemaps_url
                
        # latest update datetime
        # TODO change format datetime to 'YYYY-mm-DDTHH:MM:SSZ'
        self._details['last_update'] = str(datetime.datetime.now())

    def details(self):
        ''' return details '''
        return self._details
    
    def report(self, output=None):
        ''' website report 
        
        supported formats, defined by output: 
            None                print result to standard output
            <filename>.json     save report to json file
            <filename>.kvlite   save report to kvlite database. If the record exists, 
                                update information   
        '''
        # TODO json format
        # TODO kvlite format
        import pprint        
        pprint.pprint(self._details)

if __name__ == '__main__':
    
    import argparse
    parser = argparse.ArgumentParser(description='website info extraction')
    parser.add_argument('-u', '--url', help='website url')
    parser.add_argument('-d', '--debug', action='store_true', help='activate debug')
    
    args = parser.parse_args()
    
    if args.url:
        wsinfo = WebsiteInfo(args.url, debug=args.debug)
        wsinfo.gather()
        wsinfo.report()
    else:
        parser.print_help()


