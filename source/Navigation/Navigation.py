'''
Created on Sep 27, 2016

@author: Rahul
'''
import sys,os
sys.path.append('./Audio')

if os.name == "posix": #checks if running on Pi
    import Adafruit_PCA9685
    import RPi.GPIO as io
    import Audio
    io.setmode(io.BOARD)
    
from PipedJSON import PipedJSON
from Vector import Vector3D, Point3D
import Queue
import threading
import time
from Compass import Compass
import sys, termios
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
        self.voltage_reg_pin = 12
        self.reverse_drive_pin = 13
        io.setup(self.voltage_reg_pin,io.OUT)
        io.setup(self.reverse_drive_pin,io.OUT)

        io.output(self.voltage_reg_pin,0)
        io.output(self.reverse_drive_pin,0)
        
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
        
        self.yRotationNegativeThreshold = -0.2 #-0.075
        self.yRotationPositiveThreshold = 0.2 #0.075
        
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

        '''
        Comment out line to prevent OpenCV from opening
        '''
        self.piped_json = PipedJSON(exeName,exePath)
        
    	'''
    	PWM Driver
        60 Hz => 16.67 ms
        12 bits = 4096
        Testing servo with function generator: 0.9 ms to 2.0 ms
        16.67/4096 = 1.1/x

        Wheels turn about +/- 40 degrees => 2.53*(40/180) = 0.562
        
        '''
    	self.servo_turnTime = 0.1 #max time for servo to finish turning
        self.servo_pin = 8
        self.servo_min = 310 #280 #270
        self.servo_max = 510 #442 #510
        self.servo_range = self.servo_max - self.servo_min
        self.servo_middle = 405 #408 #self.servo_range/2 + self.servo_min #356 
        
        self.marker_leftmax_threshold = -0.562
        self.marker_rightmax_threshold = 0.562
        
        '''
        Drive Motor
        '''
        self.drive_direction = 13
        self.drive_pwm_pin = 5
        self.drive_speed = 1000
        
        '''
        Thread for stopping servo PWM
        '''
        self.startSteerTime = 0
        self.steeringTimeout = 0.3 #time for servo to finish rotating
        self.thread_servo_pwm = 0
        
        self.exitMain = False

        '''
        Variable to track last seen marker
        Boolean to see if Navigation.GetSteeringAngleRotationTranslation() thread is asleep
        '''
        self.lastSeenMarker = -1
        self.lastSeenMarkerZ = -99
        self.isAsleep = False
        self.isTurning = False

        '''
        Initialize Compass
        '''
        #self.compass = self.InitializeCompass()

        '''
        Initialize PWM Driver and Pygame Audio
        '''
        if os.name == "posix":
            try:
                self.pwm = Adafruit_PCA9685.PCA9685()
                self.pwm.set_pwm_freq(60)
                print "Resetting servo to default..."
                self.pwm.set_pwm(self.servo_pin,0,self.servo_middle)
                print "Resetting servo done!"
            except:
                print "ERROR: PWM Driver not detected"
                self.Exit()
                self.exitMain = False

            try:
                print "Initializing audio..."
                self.audioPlayer = Audio.Audio()
                print "Audio initialized!"
            except:
                print "Audio not working! Continuing anyway"
    
    def GetParsedJSON(self):
        return self.piped_json.GetParsedJSON()
        

    def Exit(self):
        print "Exitting Navigation..."
        self.piped_json.KillProcess()
        print "Resetting servo to default position..."
        if os.name == "posix":
            self.Steer(self.servo_middle)
            time.sleep(0.5)
            self.pwm.set_pwm(self.servo_pin,0,0)
            self.Stop()
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
            
            #turn left
            if yRotation <= self.yRotationNegativeThreshold:
                servoSteering = int(self.servo_middle+(self.servo_range/2)*(yRotation/(self.marker_rightmax_threshold-self.yRotationPositiveThreshold)))                
                return servoSteering
            #turn right
            elif yRotation >= self.yRotationPositiveThreshold:
                servoSteering = int(self.servo_middle+(self.servo_range/2)*(yRotation/(self.marker_rightmax_threshold-self.yRotationPositiveThreshold))) 
                return servoSteering

    def GetClosestMarker(self,parsed_JSON):
        closestMarkerNum = 0
        numberOfMarkers = len(parsed_JSON["Markers"])
        if numberOfMarkers == 1:
            return 0
        elif numberOfMarkers > 1:
            for num in range(1,numberOfMarkers):
		#print "num: " + str(num)
		#print "closest: " + str(parsed_JSON["Markers"][closestMarkerNum]["T"]["z"])
		#print "Marker at num: " + str(parsed_JSON["Markers"][num]["T"]["z"])
                if parsed_JSON["Markers"][closestMarkerNum]["T"]["z"] > parsed_JSON["Markers"][num]["T"]["z"]:
                    closestMarkerNum = num
            return closestMarkerNum
    
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
            if self.isAsleep:
                self.FlushArUcoPipe()
            else:
                parsed_JSON = self.piped_json.GetParsedJSON()
        except:
            print "\nERROR: GetParsedJSON() in method GetSteeringAngleRotationTranslation() of Navigation"
            print "Exitting all..."
            self.Exit()
            thread.exit()

        closestMarker = self.GetClosestMarker(parsed_JSON)
        
        Translation = Vector3D(Point3D(parsed_JSON["Markers"][closestMarker]["T"]["x"],parsed_JSON["Markers"][closestMarker]["T"]["y"],parsed_JSON["Markers"][closestMarker]["T"]["z"]))
        Rotation = Vector3D(Point3D(parsed_JSON["Markers"][closestMarker]["R"]["x"],parsed_JSON["Markers"][closestMarker]["R"]["y"],parsed_JSON["Markers"][closestMarker]["R"]["z"]))
        
        markerID = parsed_JSON["Markers"][closestMarker]["ID"]
         
        print "Marker: " + str(markerID) + ", " + str(Translation)
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

        '''
        Put markerID in my_queue() to pass to GUI
        '''
        #self.compass.getBearing()
        #print "compass bearing: " + str(self.compass.bearing)

        '''
        if self.isTurning:
            if markerID != 7 and Translation.Point.x >= -0.11 and Translation.Point.x <= 0.18:
                self.isTurning = False
                self.Steer(self.servo_middle)
        
        else:
        '''
        if markerID == 6:
            my_queue.put(markerID)
            self.Steer(self.servo_middle)
            self.Forward()
        elif markerID == 7:
            if Translation.Point.z <= 0.53 and not self.isTurning and not self.isAsleep:
                my_queue.put(markerID)
                #self.Steer(self.servo_min)
                #self.TurnLeft(2,self.servo_min)
                self.Steer(338)
                self.isTurning = True
                self.isAsleep = True

                self.Forward()
                time.sleep(9)
                
                self.isTurning = False
                self.isAsleep = False
                self.Steer(self.servo_middle)
                #self.TurnLeftCompass(4)
                
                print "Turning!"
            else:
                #sees marker 7 but not close enough to initiate turn
                self.Forward()
        elif markerID == 8:
            self.Steer(self.servo_max)
        elif markerID == 5:
            self.Stop()
            self.Steer(self.servo_middle)
        if self.lastSeenMarker >= 1 and self.lastSeenMarker <= 4 and self.lastSeenMarker != markerID: #check if the marker disappeared off the screen #Translation.Point.z <= 0.323:
            if self.lastSeenMarkerZ <= 0.45:
                print "Stopping at marker " + str(self.lastSeenMarker)
                my_queue.put(self.lastSeenMarker)
                self.Stop()
                self.Steer(self.servo_middle)
                self.isAsleep = True
                #time.sleep(4)
                
                if self.lastSeenMarker == 1:
                    self.audioPlayer.playAudioFile("Audio/MorrilD.wav")
                elif self.lastSeenMarker == 2:
                    self.audioPlayer.playAudioFile("Audio/ColvinR.wav")
                elif self.lastSeenMarker == 3:
                    self.audioPlayer.playAudioFile("Audio/LibraryD.wav")
                elif self.lastSeenMarker == 4:
                    self.audioPlayer.playAudioFile("Audio/WhitehurstR.wav")
                    
                self.Forward() #keep going forward until next marker triggers
                #time.sleep(1) #go forward a little so will stop reading stop
                self.isAsleep = False
                #self.FlushArUcoPipe()
            else:
                self.Forward()
        elif markerID >= 1 and markerID <= 4:
            if Translation.Point.z > 0.5:
                self.Forward()
                    

        # set lastSeenMarker
        self.lastSeenMarker = markerID
        self.lastSeenMarkerZ = Translation.Point.z
            
        '''    
        elif steeringAngle > self.servo_middle:
            my_queue.put(7) #for turning right
        #my_queue.put(6)
        #self.pwm.set_pwm(self.servo_pin,0,self.servo_min)
        elif steeringAngle < self.servo_middle:
            my_queue.put(9) #for turning left
            #my_queue.put(6)
            #self.pwm.set_pwm(self.servo_pin,0,self.servo_max)
        '''
             
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
        io.output(self.voltage_reg_pin,1)

    def VoltageReg_OFF(self):
        io.output(self.voltage_reg_pin,0)
        
    def Steer(self,steeringAngle):
        if os.name == "posix":
            self.pwm.set_pwm(self.servo_pin,0,steeringAngle)


    def Steer2(self,steeringAngle):
        if os.name == "posix":    
            self.pwm.set_pwm(self.servo_pin,0,steeringAngle)
            if self.thread_servo_pwm == 0 or not self.thread_servo_pwm.isAlive():
                self.thread_servo_pwm = threading.Thread(target=self.StopPWM,args=(time.time()))
            elif self.thread_servo_pwm.isAlive():
                self.thread_servo_pwm = threading.Thread(target=self.StopPWM,args=(time.time()))
            
            
    def StopPWM(self,startSteerTime):        
        while not time.time() - startSteerTime > self.steeringTimeout:            
            pass

        self.pwm.set_pwm(self.servo_pin,0,510)
        print "***Stopping PWM!***"
        sys.stdout.flush()
    
    def Forward(self):
        if os.name == "posix":
            self.VoltageReg_ON();
            self.pwm.set_pwm(self.drive_pwm_pin,0,self.drive_speed)

    def Stop(self):
        if os.name == "posix":
            self.VoltageReg_OFF();
            self.pwm.set_pwm(self.drive_pwm_pin,0,0)

    def TurnLeftMarker(self,leftTurnTime):
        timeLimit = time.time() + leftTurnTime
        
        initialDegree = self.GetCompassBearing()
        
        self.Steer(self.servo_min);
        self.Forward();

        self.isAsleep = True
        self.isTurning = True
        while not self.CheckIfTurned90(initialDegree):# and time.time() <= timeLimit:
            #time.sleep(0.05)
            print "InitialDegree:" + str(initialDegree) + ", Bearing: " + str(self.GetCompassBearing())
            
        self.isAsleep = False
        self.isTurning = False
        self.FlushArUcoPipe()
        
        self.Stop()
        self.Steer(self.servo_middle)
        
    
    def TurnLeftCompass(self,leftTurnTime):
        timeLimit = time.time() + leftTurnTime
        
        initialDegree = self.GetCompassBearing()
        
        self.Steer(self.servo_min);
        self.Forward();

        self.isAsleep = True
        self.isTurning = True
        while not self.CheckIfTurned90(initialDegree):# and time.time() <= timeLimit:
            #time.sleep(0.05)
            print "InitialDegree:" + str(initialDegree) + ", Bearing: " + str(self.GetCompassBearing())
            
        self.isAsleep = False
        self.isTurning = False
        self.FlushArUcoPipe()
        
        self.Stop()
        self.Steer(self.servo_middle)

    def FlushArUcoPipe(self):
        #termios.tcflush(sys.stdin, termios.TCIOFLUSH) #flush stdin so no weird lag
        #termios.tcflush(self.piped_json.GetStdout(), termios.TCIOFLUSH)
        #for line in self.piped_json.GetStdout():
        #    self.piped_json.ReadRawJSON()
        pass
    
    def TurnLeft(self,turnTime,servo_steer = None):
        if servo_steer is None:
            servo_steer = self.servo_min
        self.isAsleep = True
        self.isTurning = True
        self.Steer(servo_steer);
        self.Forward();
        time.sleep(turnTime)
        self.isAsleep = False
        self.isTurning = False
        self.FlushArUcoPipe()
        self.Stop()
        
    def TurnRight(self,turnTime,servo_steer = None):
        if servo_steer is None:
            servo_steer = self.servo_max
        self.Steer(servo_steer);
        self.Forward();
        self.isAsleep = True
        time.sleep(turnTime)
        self.isAsleep = False
        self.FlushArUcoPipe()
        self.Stop()
    
    
    '''
    Check with compass if car turned 90 degrees clockwise or counterclockwise since enclosed loop 
    '''
    def CheckIfTurned90(self,initialDegree):
        if abs(initialDegree - self.GetCompassBearing()) >= 90:
            return True
        else:
            return False
    
    def InitializeCompass(self):
        return Compass()
    
    def GetCompassBearing(self):
        return Compass().readY()
    
    def DisplayImage(self,ImageNumber):
        pass
    
    
    
#class Vector
        
        
