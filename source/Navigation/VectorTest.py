'''
Created on Sep 28, 2016

@author: Rahul
'''
import unittest
import Vector
import math
from Vector import Vector3D, Point3D

class Test(unittest.TestCase):
    
    def test_createPoints(self):
        testPoint1 = Point3D(1.200,-0.4234,10000)
        testPoint2 = Point3D(200,-111,1)
        
        print "TestPoint1: " + str(testPoint1) + ", TestPoint2: "+ str(testPoint2)
        
    def test_addVector(self):
        testPoint1 = Point3D(1,1,1)
        testPoint2 = Point3D(2,2,2)
        
        testVector1 = Vector3D(testPoint1)
        testVector2 = Vector3D(testPoint2)
        
        addedVector = testVector1.Add(testVector2)
        
        print "TestVector1: " + str(testVector1) + ",\n TestVector2: "+ str(testVector2)
        print "AddedVector: " + str(addedVector) + "\n"
        
        
        #self.assertIsInstance(testVector, Point3D)
    
    def test_distanceBetweenPoints(self):
        Point1 = Point3D(0,0,0)
        Point2 = Point3D(1,1,1)
        dist = Point1.GetDistance(Point2)
        print "Test distance between points: " + str(Point1) + " and " + str(Point2)
        print "The distance is " + str(dist)
        self.assertEqual(dist, math.sqrt(3), "Distance should be: " + str(math.sqrt(3))+". Distance was " + str(dist))
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()