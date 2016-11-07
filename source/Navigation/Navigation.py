'''
Created on Sep 27, 2016

@author: Rahul
'''
import os

if os.name == "posix": #checks if running on Pi
    import Adafruit_PCA9685
    import RPi.GPIO as io
    io.setmode(io.BOARD)
    
from PipedJSON import PipedJSON
from Vector import Vector3D, Point3D
import Queue
import thread
import time
import Compass

class Navigation(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Set up GPIO pins
        Pin 12: Ground to turn off voltage regulator
        Pin 13: Reverse drive motor
        '''
        self.io = io
        self.voltage_reg_pin = 12
        self.reverse_drive_pin = 13
        self.io.setup(self.voltage_reg_pin,self.io.OUT)
        self.io.setup(self.reverse_drive_pin,self.io.OUT)

        self.io.output(self.voltage_reg_pin,0)
        self.io.output(self.reverse_drive_pin,0)
        
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
        
        self.yRotationNegativeThreshold = -0.1 #-0.075
        self.yRotationPositiveThreshold = 0.1 #0.075
        
        if os.name == "posix":
            self.yRotationOffset = 0.1
        else:
            self.yRotationOffset = 0

        self.yRotationMin = -2.53
        self.yRotationMax = 2.53

        
        print "Navigation started! \n"
        
        '''
        subprocess.Popen opens out.exe (the C++ program)
        stdin of out.exe is piped and controlled by python
        stdout of out.exe is piped and read by python
        '''
        exeName = ""
        exePath = ""
        
        if os.name == "posix":
            exeName = "aruco_simple"
            exePath = "/home/pi/Desktop/SeniorDesign2ArUCO/build/utils/"
        else:
            exeName = "aruco_simple.exe"
            exePath = "C:/Users/Rahul/Desktop/ArUCO/SeniorDesign2ArUCO/build/bin/Release"
        
        #self.piped_json = PipedJSON(exeName,exePath)
        
    	'''
    	PWM Driver
        60 Hz => 16.67 ms
        12 bits = 4096
        Testing servo with function generator: 0.9 ms to 2.0 ms
        16.67/4096 = 1.1/x

        Wheels turn about +/- 40 degrees => 2.53*(40/180) = 0.562
        
        '''
    	self.servo_turnTime = 0.5 #max time for servo to finish turning
        self.servo_pin = 8
        self.servo_min = 310 #280 #270
        self.servo_max = 510 #442
        self.servo_range = self.servo_max - self.servo_min
        self.servo_middle = 402 #self.servo_range/2 + self.servo_min #356 
        
        self.marker_leftmax_threshold = -0.562
        self.marker_rightmax_threshold = 0.562
        
        '''
        Drive Motor
        '''
        self.drive_direction = 13
        self.drive_pwm_pin = 5
        self.drive_speed = 1500
        
        
        
        self.exitMain = False

        if os.name == "posix":
            try:
                self.pwm = Adafruit_PCA9685.PCA9685()
                self.pwm.set_pwm_freq(60)
                print "Resetting servo to default..."
                self.pwm.set_pwm(self.servo_pin,0,self.servo_middle)
                time.sleep(1)
                print "Resetting servo done!"
            except:
                print "ERROR: PWM Driver not detected"
                self.Exit()
                self.exitMain = False
    
    def GetParsedJSON(self):
        return self.piped_json.GetParsedJSON()
        

    def Exit(self):
        print "Exitting Navigation..."
        self.piped_json.KillProcess()
        print "Resetting servo to default position..."
        if os.name == "posix":
            self.pwm.set_pwm(self.servo_pin,0,self.servo_middle)
        self.exitMain = True
    
    def TestSteeringLimits(self):
        for i in xrange(510,300,-10):
            print "Steering: " + str(i) + "\n"
            self.Steer(i)
            time.sleep(0.5)
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
            +/- 180 degrees (from vector perpendicular to camera) is -2.53 and 2.53
            0   degrees (from vector perpendicular to camera) is  0.0
        
        Map y range [-2.53 to 2.53] to [0 degrees to 360 degrees]
        Force steering so yRotation is close to 0
    
        '''
        
        '''
        Calibration, 0.1 lines up for straight on, so subtract offset
        '''
        yRotation -= self.yRotationOffset
        
        if yRotation >= self.yRotationNegativeThreshold and yRotation <= self.yRotationPositiveThreshold:
            return self.servo_middle #steering is on point
        elif yRotation <= self.marker_leftmax_threshold:
            return self.servo_min
        elif yRotation >= self.marker_rightmax_threshold:
            return self.servo_max
        else:
            '''
            Return marker rotation mapped to servo rotation number
            '''
            print "Rotation: " + str(yRotation)
            
            #turn left
            if yRotation <= self.yRotationNegativeThreshold:
                servoSteering = int(self.servo_middle+(self.servo_range/2)*(yRotation/(self.marker_rightmax_threshold-self.yRotationPositiveThreshold)))                
                print "Left: " + str(servoSteering)
                return servoSteering
            #turn right
            elif yRotation >= self.yRotationPositiveThreshold:
                servoSteering = int(self.servo_middle+(self.servo_range/2)*(yRotation/(self.marker_rightmax_threshold-self.yRotationPositiveThreshold))) 
                print "Right: " + str(servoSteering)
                return servoSteering
        
    
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
        if os.name == "posix":
            self.pwm.set_pwm(self.servo_pin,0,steeringAngle)
        
        if steeringAngle > self.servo_middle:
            my_queue.put(7) #for turning right
        #my_queue.put(6)
        #self.pwm.set_pwm(self.servo_pin,0,self.servo_min)
        elif steeringAngle < self.servo_middle:
            my_queue.put(9) #for turning left
            #my_queue.put(6)
            #self.pwm.set_pwm(self.servo_pin,0,self.servo_max)
        else:
            '''
            steeringAngle == self.servo_middle, continue forward
            TODO: Add logic to check check distance z and translation to decide to continue
            forward or turn and somehow get on track
            '''
            if os.name == "posix":
                self.pwm.set_pwm(self.drive_pwm_pin,0,self.drive_speed)
            #self.pwm.set_pwm(self.servo_pin,0,self.servo_middle)
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

    def VoltageReg_ON(self):
        self.io.output(self.voltage_reg_pin,1)

    def VoltageReg_OFF(self):
        self.io.output(self.voltage_reg_pin,0)
        
    def Steer(self,steeringAngle):
        if os.name == "posix":
            self.pwm.set_pwm(self.servo_pin,0,steeringAngle)
            time.sleep(self.servo_turnTime)
            self.pwm.set_pwm(self.servo_pin,0,0)

    def Forward(self):
        if os.name == "posix":
            self.VoltageReg_ON();
            self.pwm.set_pwm(self.drive_pwm_pin,0,self.drive_speed)

    def Stop(self):
        if os.name == "posix":
            self.VoltageReg_OFF();
            self.pwm.set_pwm(self.drive_pwm_pin,0,0)
            
    def TurnLeft(self,leftTurnTime):
        timeLimit = time.time() + leftTurnTime
        
        initialDegree = self.GetCompass()
        
        self.Steer(310);
        self.Forward();
        
        while self.CheckIfTurned90(initialDegree) or time.time() > timeLimit:
            time.sleep(0.05)
            print "InitialDegree:" + str(initialDegree) + ", Bearing: " + str(self.compass.Compass.bearing)
            
        self.Stop()
    
    def TurnRight(self,rightTurnTime):
        self.Steer(510);
        self.Forward();
        time.sleep(rightTurnTime)
        self.Stop()
    
    
    '''
    Check with compass if car turned 90 degrees clockwise or counterclockwise since enclosed loop 
    '''
    def CheckIfTurned90(self,initialDegree):
        if abs(initialDegree - self.GetCompass()) >= 90:
            return True
        else:
            return False
    
    def InitializeCompass(self):
        self.compass = Compass()
    
    def GetCompass(self):
        self.compass.Compass.getBearing()
    
    def DisplayImage(self,ImageNumber):
        pass
    
    
    
#class Vector
        
        
