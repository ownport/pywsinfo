pywsinfo
========

Website info extraction. The python script is trying to collect information about website. `pywsinfo` gather information from homepage, robots.txt, sitemap.xml

```
$ python pywsinfo.py -u http://localhost:8080
{'final_url': u'http://127.0.0.1:8080/',
 'host': '127.0.0.1',
 'ip_addreses': ['127.0.0.1'],
 'keywords': ['test', 'server', 'pywsinfo'],
 'last_update': '2012-10-13 11:06:43.275387',
 'robots.txt': 'Sitemap: http://localhost:8080/sitemap.xml\nSitemap: http://localhost:8080/sitemap.xml.gz\n',
 'server': 'WSGIServer/0.1 Python/2.7.3',
 'sitemaps': ['http://localhost:8080/sitemap.xml',
              'http://localhost:8080/sitemap.xml.gz'],
 'source_url': 'http://127.0.0.1:8080',
 'status_code': 200,
 'title': 'Test server'}
```

Based on python-requests https://github.com/kennethreitz/requests

## Links

Sitemaps parsers

- [andreisavu/python-sitemap](https://github.com/andreisavu/python-sitemap)
- [varelaz / varela-python-sitemap-parser](https://github.com/varelaz/varela-python-sitemap-parser)
- [sitemaps.org](http://www.sitemaps.org/protocol.html)
- [Wikipedia:Sitemaps](http://en.wikipedia.org/wiki/Sitemaps)

