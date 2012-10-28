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
        
                
if __name__ == '__main__':
    unittest.main()        

