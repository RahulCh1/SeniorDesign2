'''
Created on Sep 27, 2016

@author: Rahul
'''
import math

class Vector3D(object):
    
    def __init__(self,Point):
        self.Point = Point
    
    def GetLength(self):
        return Point3D(0,0,0).GetDistance(self.Point)
    
    def Add(self,Vector2):
        return Vector3D(Point3D(self.Point.x + Vector2.Point.x,self.Point.y + Vector2.Point.y,self.Point.z + Vector2.Point.z))
    
    def Substract(self,Vector2):
        return Vector3D(Point3D(self.Point.x - Vector2.Point.x,self.Point.y - Vector2.Point.y,self.Point.z - Vector2.Point.z))
    
    def CrossProduct(self,Vector2):
        '''
            i    j    k
            a    b    c
            d    e    f
            
            <b*f - c*e, (-1)(a*f - c*d), a*e - b*d>
        '''
        a = self.Point.x
        b = self.Point.y
        c = self.Point.z
        
        d = Vector2.Point.x
        e = Vector2.Point.y
        f = Vector2.Point.z
        
        Point = Point3D(b*f-c*e,-1*(a*f-c*d),a*e-b*d)
        return Point
        
    def DotProduct(self,Vector2):
        return self.Point.x * Vector2.Point.x + self.Point.y * Vector2.Point.y + self.Point.z * Vector2.Point.z
    
    def GetAngleBetweenVectors(self,Vector2):
        return math.acos(self.DotProduct(Vector2)/(self.GetLength()*Vector2.GetLength()))
    
    def UnitVector(self):
        length = self.GetLength()
        return Vector3D(Point3D(self.Point.x/length,self.Point.y/length,self.Point.z/length))
    
    def __str__(self):
        return "<" + str(self.Point.x) + ", " + str(self.Point.y) + ", " + str(self.Point.z) + ">"

class Point3D(object):
    '''
    classdocs
    '''

    def __init__(self, x, y, z):
        '''
        Constructor
        '''
        self.x = float(x);
        self.y = float(y);
        self.z = float(z);
        
    def GetDistance(self,Vector2):
        return math.sqrt(math.pow(self.x-Vector2.x, 2)+math.pow(self.y-Vector2.y, 2)+math.pow(self.z-Vector2.z, 2))
    
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"