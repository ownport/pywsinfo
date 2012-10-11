import socket
import pywsinfo
import unittest

class WebSiteUtilsTests(unittest.TestCase):

    def test_parse_url(self):
        
        url = 'http://www.example.com'
        self.assertEqual(
                pywsinfo.parse_url(url),  
                {'website.url': 'http://www.example.com', 'website.host': 'www.example.com'}
        )
        url = 'http://www.example.com/path'
        self.assertEqual(
                pywsinfo.parse_url(url),  
                {'website.url': 'http://www.example.com', 'website.host': 'www.example.com'}
        )
        url = 'http://www.example.com/path?12&12'
        self.assertEqual(
                pywsinfo.parse_url(url),  
                {'website.url': 'http://www.example.com', 'website.host': 'www.example.com'}
        )
        url = 'https://www.example.com'
        self.assertEqual(
                pywsinfo.parse_url(url),  
                {'website.url': 'https://www.example.com', 'website.host': 'www.example.com'}
        )

    def test_nsloopup(self):
        
        self.assertGreater(len(pywsinfo.nslookup('google.com')), 1)        
        self.assertGreater(len(pywsinfo.nslookup('www.google.com')), 1)        
        self.assertRaises(socket.gaierror, pywsinfo.nslookup, 'www.google.com2')

        
if __name__ == '__main__':
    unittest.main()        

