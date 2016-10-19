'''
Created on Sep 27, 2016

@author: Rahul
'''
from Vector import Vector3D, Point3D
import Navigation
#source: http://stackoverflow.com/questions/36748829/piping-binary-data-between-python-and-c
import subprocess

if __name__ == '__main__':
    myNav = Navigation.Nav()
    
    '''
        Ranges:
        Rotation x: -3.3 to 3.52
        Rotation y: -0.15 to 0.27
        Rotation z: -0.56 to 0.61
        
        Translation x: -0.27 to 0.26 
        Translation y: -0.20 to 0.18
        Translation z: 0 to 2.61
    '''
    
    leftXThreshold = -0.10
    rightXThreshold = 0.10
    
    backwardZThreshold = 0.7;
    forwardZThreshold = 2;
    
    print "Please give the input as format: x y z \n"
    while True:
        consoleInputID = raw_input("Marker ID: \n")
        
        #stop and play images if IDs correspond to 1 through 5, else continue
        if int(consoleInputID) >= 1 and int(consoleInputID) <= 5:
            print "Stop and display images \n"
            continue
        
        consoleInputT = raw_input("Translation Vector: \n")
        consoleInputR = raw_input("Rotation Vector: \n")
        
        #splits on white space
        TArray = consoleInputT.split()
        RArray  = consoleInputR.split()
        
        if len(TArray) == 3 and len(RArray) == 3:
            
            if int(consoleInputID) >= 1 and int(consoleInputID) <= 5:
                print "Stop and display images \n"
            
            TPoint = Vector3D(Point3D(float(TArray[0]),float(TArray[1]),float(TArray[2])))
            RPoint = Vector3D(Point3D(float(RArray[0]),float(RArray[1]),float(RArray[2])))
            
            print myNav.GetSteeringAngleRotationTranslation(TPoint,RPoint)
        else:
            print "Bad Input! \n"
            continue

class Nav(object):
    '''
    classdocs
    '''
    from Vector import Vector3D, Point3D
    #def __init__(self, CameraPosition, CameraRotation, MarkerPosition, MarkerRotation):
    def __init__(self):
        '''
        Constructor
        '''
        print "Navigation started! \n"
        
        '''
        subprocess.Popen opens out.exe (the C++ program)
        stdin of out.exe is piped and controlled by python
        stdout of out.exe is piped and read by python
        '''
        proc = subprocess.Popen("C:/Users/Rahul/Desktop/ArUCO/SeniorDesign2ArUCO/build/bin/Release/aruco_simple.exe",cwd=r'C:/Users/Rahul/Desktop/ArUCO/SeniorDesign2ArUCO/build/bin/Release/',stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        
        '''
        It works! The C program was hanging on imread("../../resources/leftArrow.png") because the 
        current working directory was not set as where the executable is being called from.
        Fixed by setting cwd (current working directory) in Popen
        source: http://stackoverflow.com/questions/1685157/python-specify-popen-working-directory-via-argument
        '''
        
        i = 0
        while i < 100:
            message = proc.stdout.readline()
            message = message.strip() #remove blanks
            if message != '':
                i += 1
                print str(i) +": " + message
        
        
        '''
        Popen.wait() waits for the child process to terminate
        Popen.kill() kills the child process
        '''
        proc.kill()
    
    '''
    Get JSON from OpenCV
    '''
    def ParseJSON(self):
        pass    
    
    '''
    Might Implement later
    Get the angle to steer in depending on angle between axis of Camera and Marker
    '''
    def GetSteeringAnglePose(self,CameraPose,MarkerPose):
        pass
    
    '''
    Get the steering angle (in the future) based on the Rotation and Translation vector from the center of the Camera to center of Marker 
    '''
    def GetSteeringAngleRotationTranslation(self,Translation,Rotation):
        '''
        Ranges:
        Rotation x: -3.3 to 3.52
        Rotation y: -0.15 to 0.27
        Rotation z: -0.56 to 0.61
        
        Translation x: -0.27 to 0.26
        Translation y: -0.20 to 0.18
        Translation z: 0 to 2.61
        '''
        #real thresholds
#         leftXThreshold = -0.10
#         rightXThreshold = 0.10
#         
#         backwardZThreshold = 0.7
#         forwardZThreshold = 2
        
        # fake thresholds for testing
        leftXThreshold = -1
        rightXThreshold = 1
        
        backwardZThreshold = -1
        forwardZThreshold = 1
        
        toReturnStr = ""
        
        if Translation.Point.x <= leftXThreshold:
            toReturnStr = toReturnStr + "Turn left \n"
            #return 9; #for turning left
        if Translation.Point.x >= rightXThreshold:
            toReturnStr = toReturnStr + "Turn right \n"
            #return 7; #for turning right
        if Translation.Point.z <= backwardZThreshold:
            toReturnStr = toReturnStr + "Go forward \n"
            #return 8; #for going backward
        if Translation.Point.z >= forwardZThreshold:
            toReturnStr = toReturnStr + "Go backward \n"
        else:
            toReturnStr = "Stop"
        
        #CameraOrientation = Vector3D(Point3D(2,2,2))
        
        
        #toReturnStr = toReturnStr + "Angle from origin: " +  str(CameraOrientation.GetAngleBetweenVectors(Translation))
        
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
        
        