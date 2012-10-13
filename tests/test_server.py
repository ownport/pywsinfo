#!/usr/bin/env python

import os
import sys
import logging

from packages import bottle
from packages import pyservice

# default variables

STATIC_FILES_DIR =os.path.join(os.getcwd(), 'tests/static')

# monkey patching for BaseHTTPRequestHandler.log_message
def log_message(obj, format, *args):
    logging.info("%s %s" % (obj.address_string(), format%args))

# Application

@bottle.route('/')
def index():
    return ''' 
    <html>
        <head>
            <title>Test server</title>
            <meta name="keywords" content="test,server,pywsinfo"/>
            <meta name="description" content="server for testing pywsinfo"
        </head>
        <body>pywsinfo test server</body>
    </html>
    '''

@bottle.get('/favicon.ico')
def get_robotstxt():
    return bottle.static_file('favicon.ico', root=STATIC_FILES_DIR)


@bottle.get('/robots.txt')
def get_robotstxt():
    return bottle.static_file('robots.txt', root=STATIC_FILES_DIR)

# Process to run
class BottleProcess(pyservice.Process):

    pidfile = os.path.join(os.getcwd(), 'tests/run/test_server.pid')
    logfile = os.path.join(os.getcwd(), 'tests/log/test_server.log')

    def __init__(self):
        super(BottleProcess, self).__init__()
        
        from BaseHTTPServer import BaseHTTPRequestHandler
        BaseHTTPRequestHandler.log_message = log_message
            
    def run(self):
        logging.info('Bottle {} server starting up'.format(bottle.__version__))
        bottle.debug(True)
        bottle.run(host='localhost', port=8080)

if __name__ == '__main__':

    if len(sys.argv) == 2 and sys.argv[1] in 'start stop restart status'.split():
        pyservice.service('test_server.BottleProcess', sys.argv[1])
    else:
        print 'usage: bottled <start,stop,restart,status>'
