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

        tag = 'urlset'     
        self.assertEqual(pywsinfo.SitemapParser._plain_tag(tag), 'urlset')

        tag = 'sitemap'     
        self.assertEqual(pywsinfo.SitemapParser._plain_tag(tag), 'sitemap')

    def test_get_success(self):
        
        sitemap_urls = (
            'http://localhost:8080/sitemap.xml',
            'http://localhost:8080/sitemap.text.xml',
            'http://localhost:8080/sitemap.text.utf-8.xml',
            'http://localhost:8080/sitemap.xml.gz',
        )
        for url in sitemap_urls:
            parser = pywsinfo.SitemapParser(url)
            parser.parse()
        
    def test_get_unsuccess(self):
        
        sitemap_urls = (
            'http://localhost:8080/sitemap',
        )
        for url in sitemap_urls:
            parser = pywsinfo.SitemapParser(url)
            parser.parse()

    def test_sitemap_index(self):
        
        sitemap_urls = (
            'http://localhost:8080/sitemap_index.xml',
        )
        for url in sitemap_urls:
            parser = pywsinfo.SitemapParser(url)
            parser.parse()
    
                    

        
if __name__ == '__main__':
    unittest.main()        

