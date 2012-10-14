import socket
import pywsinfo
import unittest

class SitemapParserTests(unittest.TestCase):

    def test_sitemap_parser_init(self):
        
        parser = pywsinfo.SitemapParser('http://www.example.com/sitemap.xml')
        parser = pywsinfo.SitemapParser([
                        'http://www.example.com/sitemap1.xml',
                        'http://www.example.com/sitemap2.xml',
                        'http://www.example.com/sitemap3.xml',
        ])
        parser = pywsinfo.SitemapParser((
                        'http://www.example.com/sitemap1.xml',
                        'http://www.example.com/sitemap2.xml',
                        'http://www.example.com/sitemap3.xml',
        ))
        self.assertRaises(RuntimeError, pywsinfo.SitemapParser, (123))

    def test_plain_tag(self):
        
        tag = '{http://www.sitemaps.org/schemas/sitemap/0.9}urlset'     
        self.assertEqual(pywsinfo.SitemapParser._plain_tag(tag), 'urlset')

        tag = '{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap'     
        self.assertEqual(pywsinfo.SitemapParser._plain_tag(tag), 'sitemap')

        
if __name__ == '__main__':
    unittest.main()        

