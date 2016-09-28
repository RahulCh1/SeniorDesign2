'''
Created on Sep 27, 2016

@author: Rahul
'''
import math

class Vector3D(object):
    
    def __init__(self,Point):
        self = Point
    
    def GetLength(self):
        return self.GetDistance(Point3D(0,0,0))
    
    def Add(self,Vector2):
        return Vector3D(Point3D(self.x + Vector2.x,self.y + Vector2.y,self.z + Vector2.z))
    
    def Substract(self,Vector2):
        return Vector3D(Point3D(self.x - Vector2.x,self.y - Vector2.y,self.z - Vector2.z))
    
    def CrossProduct(self,Vector2):
        '''
            i    j    k
            a    b    c
            d    e    f
            
            <b*f - c*e, (-1)(a*f - c*d), a*e - b*d>
        '''
        a = self.x
        b = self.y
        c = self.z
        
        d = Vector2.x
        e = Vector2.y
        f = Vector2.z
        
        Point = Point3D(b*f-c*e,-1*(a*f-c*d),a*e-b*d)
        return Point
        
    def DotProduct(self,Vector2):
        return self.x * Vector2.x + self.y * Vector2.y + self.z * Vector2.z
        
    def __str__(self):
        return ""

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