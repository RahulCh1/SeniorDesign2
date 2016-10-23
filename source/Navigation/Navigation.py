'''
Created on Sep 27, 2016

@author: Rahul
'''
from PipedJSON import PipedJSON
from Vector import Vector3D, Point3D
import Queue
import thread

class Navigation(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        
        '''
        Ranges:
        Rotation x: -3.3 to 3.52
        Rotation y: -2.53 to 2.53
        Rotation z: -0.56 to 0.61
        
        Translation x: -0.27 to 0.26 
        Translation y: -0.20 to 0.18
        Translation z: 0 to 2.61
        '''
    
        self.leftXThreshold = -0.10
        self.rightXThreshold = 0.10
        
        self.backwardZThreshold = 0.7
        self.forwardZThreshold = 2
        
        self.yRotationNegativeThreshold = -0.075
        self.yRotationPositiveThreshold = 0.075
        self.yRotationOffset = 0.1
        
        
        print "Navigation started! \n"
        
        '''
        subprocess.Popen opens out.exe (the C++ program)
        stdin of out.exe is piped and controlled by python
        stdout of out.exe is piped and read by python
        '''
        self.piped_json = PipedJSON("aruco_simple.exe","C:/Users/Rahul/Desktop/ArUCO/SeniorDesign2ArUCO/build/bin/Release")
        
        self.exitMain = False
    
    def GetParsedJSON(self):
        return self.piped_json.GetParsedJSON()
    
    
    def Exit(self):
        print "Exitting Navigation..."
        self.piped_json.KillProcess()
        self.exitMain = True
        
    '''
    Might Implement later
    Get the angle to steer in depending on angle between axis of Camera and Marker
    '''
    def GetMappedSteeringAngle(self,yRotation):
        '''
        Rotation of y range:
            -2.53 to 2.53
            CCW is negative
            CW is positive
            180 degrees (from vector perpendicular to camera) is -2.53 and 2.53
            0   degrees (from vector perpendicular to camera) is  0.0
        
        Map y range [-2.53 to 2.53] to [0 degrees to 360 degrees]
        Force steering so yRotation is close to 0
    
        '''
        
        '''
        Calibration, 0.1 lines up for straight on, so subtract offset
        '''
        yRotation -= self.yRotationOffset
        
        if yRotation >= self.yRotationNegativeThreshold and yRotation <= self.yRotationPositiveThreshold:
            return 0 #steering is on point
        elif yRotation < -0.1:
            return (yRotation/-2.53)*-180
        else:
            return (yRotation/2.53)*180
        
    
    '''
    Get the steering angle (in the future) based on the Rotation and Translation vector from the center of the Camera to center of Marker
    Stores GUI picture number in queue (a mutable object) by a Thread of this method which is retrieved in main later
    '''
    def GetSteeringAngleRotationTranslation(self,my_queue):
        '''
        Ranges:
        Rotation x: -3.3 to 3.52
        Rotation y: -2.53 to 2.53
        Rotation z: -0.56 to 0.61
        
        Translation x: -0.27 to 0.26
        Translation y: -0.20 to 0.18
        Translation z: 0 to 2.61
        '''
        try:
            parsed_JSON = self.piped_json.GetParsedJSON()
        except:
            print "\nERROR: GetParsedJSON() in method GetSteeringAngleRotationTranslation() of Navigation"
            print "Exitting all..."
            self.Exit()
            thread.exit()
            
        Translation = Vector3D(Point3D(parsed_JSON["Markers"][0]["T"]["x"],parsed_JSON["Markers"][0]["T"]["y"],parsed_JSON["Markers"][0]["T"]["z"]))
        Rotation = Vector3D(Point3D(parsed_JSON["Markers"][0]["R"]["x"],parsed_JSON["Markers"][0]["R"]["y"],parsed_JSON["Markers"][0]["R"]["z"]))
        
        
        '''
        Get steering angle
        '''
        #print "Steering angle: " + str(self.GetMappedSteeringAngle(Rotation.Point.y)) + ", " + str(Rotation.Point.y)
        steeringAngle = self.GetMappedSteeringAngle(Rotation.Point.y)
                
        '''
        Put number in queue for displaying appropriate GUI image
        '''
        
#         if Translation.Point.x <= self.leftXThreshold:
#             my_queue.put(9) #for turning left
#         if Translation.Point.x >= self.rightXThreshold:
#             my_queue.put(7) #for turning right

        
        '''
        TODO: Get time lapsed between each detected marker so can decide whether or not markers
        are in field of view or if lost track for quite some time.
        Issues with this approach: Getting parsed_JSON is also blocking. Also calling this method from thread.
        Resolution to this approach: Use boolean flag on Navigation which is set when method thread runs out of time to execute
        Alternative approach issue: Cannot change C++ code to send blanks because MDetector.detect() is also blocking
        '''
        
        
        if steeringAngle > 0:
            my_queue.put(7) #for turning right
        elif steeringAngle < 0:
            my_queue.put(9)
        else:
            '''
            steeringAngle == 0, continue forward
            TODO: Add logic to check check distance z and translation to decide to continue
            forward or turn and somehow get on track
            '''
            my_queue.put(6)
                
#         if Translation.Point.z <= self.backwardZThreshold:
#             my_queue.put(8) #for going backward
#         if Translation.Point.z >= self.forwardZThreshold:
#             my_queue.put(6) #for going forward
#         else:
#             my_queue.put(5) #for default stop sign
    
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
        
        