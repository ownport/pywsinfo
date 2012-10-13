import pywsinfo
import unittest

class WebSiteInfoTests(unittest.TestCase):
    
    def test_main(self):
        wsinfo = pywsinfo.WebsiteInfo('http://localhost:8080')
        wsinfo.run()
        
                
if __name__ == '__main__':
    unittest.main()        

