'''
Created on Sep 27, 2016

@author: Rahul
'''
from PipedJSON import PipedJSON
from Vector import Vector3D, Point3D

class Navigation(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        
        '''
        Ranges:
        Rotation x: -3.3 to 3.52
        Rotation y: -0.15 to 0.27
        Rotation z: -0.56 to 0.61
        
        Translation x: -0.27 to 0.26 
        Translation y: -0.20 to 0.18
        Translation z: 0 to 2.61
        '''
    
        self.leftXThreshold = -0.10
        self.rightXThreshold = 0.10
        
        self.backwardZThreshold = 0.7
        self.forwardZThreshold = 2
    
        print "Navigation started! \n"
        
        '''
        subprocess.Popen opens out.exe (the C++ program)
        stdin of out.exe is piped and controlled by python
        stdout of out.exe is piped and read by python
        '''
        self.piped_json = PipedJSON("aruco_simple.exe","C:/Users/Rahul/Desktop/ArUCO/SeniorDesign2ArUCO/build/bin/Release")
        
    
    def GetParsedJSON(self):
        return self.piped_json.GetParsedJSON()
    
    
    def Exit(self):
        print "Exitting Navigation..."
        self.piped_json.KillProcess()
        
    '''
    Might Implement later
    Get the angle to steer in depending on angle between axis of Camera and Marker
    '''
    def GetSteeringAnglePose(self,CameraPose,MarkerPose):
        pass
    
    '''
    Get the steering angle (in the future) based on the Rotation and Translation vector from the center of the Camera to center of Marker 
    '''
    def GetSteeringAngleRotationTranslation(self):
        '''
        Ranges:
        Rotation x: -3.3 to 3.52
        Rotation y: -0.23 to 0.23
        Rotation z: -0.56 to 0.61
        
        Translation x: -0.27 to 0.26
        Translation y: -0.20 to 0.18
        Translation z: 0 to 2.61
        '''
        parsed_JSON = self.piped_json.GetParsedJSON()
        Translation = Vector3D(Point3D(parsed_JSON["Markers"][0]["T"]["x"],parsed_JSON["Markers"][0]["T"]["y"],parsed_JSON["Markers"][0]["T"]["z"]))
        
        toReturnStr = ""
        
        if Translation.Point.x <= self.leftXThreshold:
            toReturnStr = toReturnStr + "Turn left \n"
            return 9 #for turning left
        if Translation.Point.x >= self.rightXThreshold:
            toReturnStr = toReturnStr + "Turn right \n"
            return 7 #for turning right
        if Translation.Point.z <= self.backwardZThreshold:
            toReturnStr = toReturnStr + "Go forward \n"
            return 8 #for going backward
        if Translation.Point.z >= self.forwardZThreshold:
            toReturnStr = toReturnStr + "Go backward \n"
            return 6 #for going forward
        else:
            toReturnStr = "Stop"
            return 5 #for default stop sign
     
        return toReturnStr
        
        
    
    '''
    Maybe unnecessary to find error. Can just get angle difference and act on that.
    '''
    def MinimizeError(self):
        pass
    
    def TurnLeft(self,SteeringAngle):
        pass
    
    def TurnRight(self,SteeringAngle):
        pass
    
    def Stop(self):
        pass
    
    def Forward(self,Speed):
        pass
    
    '''
    Check with compass if car turned 90 degrees clockwise or counterclockwise since enclosed loop 
    '''
    def CheckIfTurned90(self):
        #GetCompass here
        pass
    
    def GetCompass(self):
        pass
    
    def DisplayImage(self,ImageNumber):
        pass
    
    
    
#class Vector
        
        