#!/usr/bin/env python
#
#   Website info gathering
#

# TODO extract meta information from homepage (head, meta)
# TODO add robots.txt support
# TODO add sitemap.xml support
# TODO add choice to select different reports about website

__author__  = 'Andrey Usov <https://github.com/ownport/pywsinfo>'
__version__ = '0.1'

import requests

class WebsiteInfo(object):
    ''' website information '''    
    
    def __init__(self, website_url):    
        self._website_url = website_url
        self._website_details = dict()
        self._parse_url(self._website_url)

    def _parse_url(self, url):  
        print self._website_url    
    
    def _make_head_request(self, url):
        pass
    
    def _make_get_request(self, url):
        pass

    def run(self):
        ''' run website info retrieval '''
        pass

    def report(self):
        pass

if __name__ == '__main__':
    
    import argparse
    parser = argparse.ArgumentParser(description='website info extraction')
    parser.add_argument('-u', '--url', help='website url')
    
    args = parser.parse_args()
    
    if args.url:
        wsinfo_process = WebsiteInfo(args.url)
        wsinfo_process.run()
    else:
        parser.print_help()


