pywsinfo
========

Website info extraction. The python script is trying to collect information about website. `pywsinfo` gather information from homepage, robots.txt, sitemap.xml

```
$ python pywsinfo.py -u http://www.example.com
{'final_url': u'http://www.example.com/',
 'host': 'www.example.com',
 'ip_addreses': ['xxx.xxx.xxx.xxx'],
 'keywords': ['web',
              'site',
              'example'],
 'last_update': '2012-10-12 10:50:09.166641',
 'robots.txt': 'Sitemap: http://www.example.com/sitemap.xml\n\nUser-agent: *\nDisallow: /private\nCrawl-delay: 1\n\n',
 'sitemaps': ['http://www.example.com/sitemap.xml'],
 'source_url': 'http://www.example.com',
 'status_code': 200,
 'title': 'Example.com'}
```

Based on python-requests https://github.com/kennethreitz/requests

## Links

Sitemaps parsers

- [andreisavu/python-sitemap](https://github.com/andreisavu/python-sitemap)
- [varelaz / varela-python-sitemap-parser](https://github.com/varelaz/varela-python-sitemap-parser)
