'''
Created on Sep 27, 2016

@author: Rahul
'''
import unittest
import time
from Navigation import Navigation

class Test(unittest.TestCase):

    '''
    Only one test works each time or C++ crashes
    '''
#     def test_Navigation_init(self):
#         print "Test 1 Started \n"
#         myNav = Navigation()
#         time.sleep(1)
#         myNav.Exit()
#         time.sleep(1)
#         print "Test 1 Ended \n"
    
    def test_Navigation_direction(self):
        print "Test 2 Started \n"
        myNav2 = Navigation()
        print "Direction to turn (int): " + str(myNav2.GetSteeringAngleRotationTranslation())
        myNav2.Exit()
        print "Test 2 Ended \n"
     
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()