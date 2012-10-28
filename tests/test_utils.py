import sys
if '' not in sys.path:
    sys.path.append('')

import pywsinfo
import unittest

class WebSiteUtilsTests(unittest.TestCase):

    def test_parse_url(self):
        
        url = 'http://www.example.com'
        self.assertEqual(
                pywsinfo.parse_url(url),  
                {'source_url': 'http://www.example.com', 'host': 'www.example.com'}
        )
        url = 'http://www.example.com/path'
        self.assertEqual(
                pywsinfo.parse_url(url),  
                {'source_url': 'http://www.example.com', 'host': 'www.example.com'}
        )
        url = 'http://www.example.com/path?12&12'
        self.assertEqual(
                pywsinfo.parse_url(url),  
                {'source_url': 'http://www.example.com', 'host': 'www.example.com'}
        )
        url = 'https://www.example.com'
        self.assertEqual(
                pywsinfo.parse_url(url),  
                {'source_url': 'https://www.example.com', 'host': 'www.example.com'}
        )
        url = 'http://localhost:8080'
        self.assertEqual(
                pywsinfo.parse_url(url),  
                {'source_url': 'http://localhost:8080', 'host': 'localhost'}
        )

    def test_nsloopup(self):
        
        self.assertGreater(len(pywsinfo.nslookup('google.com')), 1)        
        self.assertGreater(len(pywsinfo.nslookup('www.google.com')), 1)        
        self.assertEqual(pywsinfo.nslookup('www.google.com2'), [])

    def test_parse_html_head(self):
        
        html = '''<head> 
                    <meta name="Keywords" content="keyword1,keyword2"> 
                    <meta name="Description" content="description">
                </head>'''
        self.assertEqual(pywsinfo.parse_html_head(html), 
                        {'keywords':['keyword1','keyword2'], 'description': 'description'})

        html = '''<head> 
                    <meta name="keywords" content="keyword1,keyword2"> 
                    <meta name="description" content="description">
                </head>'''
        self.assertEqual(pywsinfo.parse_html_head(html), 
                        {'keywords':['keyword1','keyword2'], 'description': 'description'})

        html = '''<head> 
                    <meta name="keywords" content=""> 
                    <meta name="description" content="">
                </head>'''
        self.assertEqual(pywsinfo.parse_html_head(html), {})

        html = '''<head></head>'''
        self.assertEqual(pywsinfo.parse_html_head(html), {})

        
if __name__ == '__main__':
    unittest.main()        

