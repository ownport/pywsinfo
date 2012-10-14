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
import pprint
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
    '{http://www.sitemaps.org/schemas/sitemap/0.9}',
)


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
#   SitemapParser
# -----------------------------------------------
class SitemapParser(object):
    
    def __init__(self, sitemap, debug=False):
        ''' init 
        
        sitemap can be as one url or as list of urls to sitemaps
        '''
        self._debug = debug
        self._urls = list()
        self._sitemap_urls = list()
        if isinstance(sitemap, (str,unicode)):
            self._sitemap_urls.append(sitemap)
        elif isinstance(sitemap, (list,tuple)):
            self._sitemap_urls.extend(sitemap)
        else:
            raise RuntimeError('Unknow sitemap type: {}'.format(type(sitemap)))

    @staticmethod
    def _plain_tag(tag):
        ''' remove namespaces and returns tag '''

        for namespace in NAMESPACES:
            if tag.find(namespace) >= 0:
                return tag.replace(namespace,'')
        return tag

    def _get(self, url):
        ''' get sitemap, if it compressed -> decompress'''
        SUPPORTED_PLAIN_CONTENT_TYPE = (
            'text/xml', 'application/xml',
        )
        SUPPORTED_COMPESSES_CONTENT_TYPE = (
            'application/octet-stream', 'application/x-gzip',
        )
        resp = requests.get(url)
        if resp.status_code == 200:
            content_type = resp.headers['content-type'].lower()
            if ';' in content_type:
                content_type = content_type.split(';')[0]
            if content_type in SUPPORTED_PLAIN_CONTENT_TYPE:
                return resp.content
            elif content_type in SUPPORTED_COMPESSES_CONTENT_TYPE:
                return GzipFile(fileobj=StringIO(resp.content)).read()
        return None

    def _parse_urlset(self, tree):
        ''' parse sitemap if there's urlset, 
        returns the list of url details:
            - loc (required)
            - lastmod (optional)
            - changefreq (optional)
            - priority (optional)'''
            
        for url in tree:
            url = dict([(self._plain_tag(param.tag), param.text) for param in url])
            yield url

    def _parse_sitemap_index(self, tree):
        ''' parse sitemap if there's sitemapindex, 
        returns the list of url to sitemaps '''

        for sitemap in tree:
            url = dict([(self._plain_tag(param.tag), param.text) for param in sitemap])
            yield url['loc']

    def _parse_sitemap(self, sitemap):
        ''' parse sitemap 
        and return the list of (loc, lastmod, priority)'''
        
        urls = list()
        root = xml_parser.fromstring(sitemap)
        
        if self._plain_tag(root.tag) == 'sitemapindex':
            self._sitemap_urls.extend(self._parse_sitemap_index(root))
            
        if self._plain_tag(root.tag) == 'urlset':
            urls.extend(self._parse_urlset(root))
            
        return urls

    def parse(self):
        ''' parse sitemap, if there's more than one sitemap url, the data will be merged '''        

        while True:
            try:
                sitemap_url = self._sitemap_urls.pop()
            except IndexError:
                break
            sitemap = self._get(sitemap_url)
            if sitemap:
                # self._urls.extend(self._parse_sitemap(sitemap))
                # print self._parse_sitemap(sitemap)
                for url in self._parse_sitemap(sitemap):
                    print url['loc']

    def report(self):
        ''' report  '''
        pprint.pprint(self._urls)

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

    def run(self):
        ''' run website info retrieval '''
        
        # nslookup
        self._details['ip_addreses'] = nslookup(self._details['host'])

        # first request to web site. Try to detect 
        if len(self._details['ip_addreses']) > 0:
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
                        self._details['sitemaps'].append(line.replace('Sitemap:', '').strip())

        # check default sitemap
        if 'sitemaps' not in self._details:
            sitemaps_url = urlparse.urljoin(self._details['final_url'],'/sitemap.xml')
            resp = self._make_request('HEAD', sitemaps_url) 
            if resp['status_code'] == 200:
                self._details['sitemaps'] = sitemaps_url
                
        # latest update datetime
        # TODO change format datetime to 'YYYY-mm-DDTHH:MM:SSZ'
        self._details['last_update'] = str(datetime.datetime.now())
    
    def report(self):
        ''' website report '''
        
        pprint.pprint(self._details)

if __name__ == '__main__':
    
    import argparse
    parser = argparse.ArgumentParser(description='website info extraction')
    parser.add_argument('-u', '--url', help='website url')
    parser.add_argument('-s', '--sitemap', help='get sitemap content')
    parser.add_argument('-d', '--debug', action='store_true', help='activate debug')
    
    args = parser.parse_args()
    
    if args.url:
        wsinfo = WebsiteInfo(args.url, debug=args.debug)
        wsinfo.run()
        wsinfo.report()
    elif args.sitemap:
        sitemap_parser = SitemapParser(args.sitemap, debug=args.debug)
        sitemap_parser.parse()
    else:
        parser.print_help()


