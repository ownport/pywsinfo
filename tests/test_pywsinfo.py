import sys
if '' not in sys.path:
    sys.path.append('')

import pywsinfo
import unittest

class WebSiteInfoTests(unittest.TestCase):
    
    def test_main(self):
        wsinfo = pywsinfo.WebsiteInfo('http://localhost:8080')
        wsinfo.gather()

        wsinfo = pywsinfo.WebsiteInfo('http://.:8080')
        self.assertRaises(RuntimeError, wsinfo.gather)

    def test_get_details(self):
        wsinfo = pywsinfo.WebsiteInfo('http://localhost:8080')
        wsinfo.gather()
        details = wsinfo.details()
        self.assertEqual(details['status_code'], 200)
            
                
if __name__ == '__main__':
    unittest.main()        

