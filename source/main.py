'''
Created on Sep 28, 2016

@author: Rahul
'''
import os, sys
import threading 
import Queue
import time
# Add current dir to search path.
# sys.path.insert(0, "GUI")
# sys.path.insert(1, "Navigation")
sys.path.append('GUI')
sys.path.append('Navigation')

import GuiDisplay as gui

from Navigation import Navigation

if __name__ == '__main__':
    
    #start navigation
    myNavigation = Navigation()
    servo_middle = 402
    pulseTime = 0.5
    
    print "servo_max: " + str(myNavigation.servo_max)
    print "servo_min: " + str(myNavigation.servo_min)

    '''
    myNavigation.pwm.set_pwm(myNavigation.servo_pin,0,myNavigation.servo_middle)
    time.sleep(3)
    myNavigation.pwm.set_pwm(myNavigation.servo_pin,0,myNavigation.servo_min)
    time.sleep(3)
    myNavigation.pwm.set_pwm(myNavigation.servo_pin,0,myNavigation.servo_max)
    time.sleep(3)
    '''
    
    
    print "Center and right\n"

    '''
    #center 525 humming, 510 no hum
    myNavigation.Steer(servo_middle)
    time.sleep(3)
    myNavigation.Steer(myNavigation.servo_max+70+15)
    print "New Max: " + str(myNavigation.servo_max+70+15)
    time.sleep(10)
    '''
    #310 to 510
    for i in xrange(510,300,-10):
        print "Steering: " + str(i) + "\n"
        myNavigation.Steer(i)
        time.sleep(0.5)
    
    
    '''
    print "Starting right turn"
    myNavigation.Forward()
    time.sleep(7)
    myNavigation.Stop()
    '''
    
    
    '''
    print "Left\n"
    #right
    myNavigation.pwm.set_pwm(myNavigation.servo_pin,0,myNavigation.servo_min)
    time.sleep(pulseTime)
    myNavigation.pwm.set_pwm(myNavigation.servo_pin,0,0)
    time.sleep(3)

    print "Right\n"
    #left
    myNavigation.pwm.set_pwm(myNavigation.servo_pin,0,myNavigation.servo_max)
    time.sleep(pulseTime)
    myNavigation.pwm.set_pwm(myNavigation.servo_pin,0,0)
    time.sleep(3)
    '''
    
    print "***Done!***"
    '''
    myNavigation.pwm.set_pwm(myNavigation.drive_pwm_pin,0,1500)
    time.sleep(15)
    myNavigation.pwm.set_pwm(myNavigation.drive_pwm_pin,0,0)
    time.sleep(2)
    '''
    
    '''
    print "Go Left"
    myNavigation.pwm.set_pwm(myNavigation.servo_pin,0,myNavigation.servo_min)
    time.sleep(3)
    myNavigation.pwm.set_pwm(myNavigation.drive_pwm_pin,0,1500)
    time.sleep(5)
    myNavigation.pwm.set_pwm(myNavigation.drive_pwm_pin,0,0)
    time.sleep(2)

    print "Go Right"
    myNavigation.pwm.set_pwm(myNavigation.servo_pin,0,myNavigation.servo_max)
    time.sleep(3)
    myNavigation.pwm.set_pwm(myNavigation.drive_pwm_pin,0,1500)
    time.sleep(5)
    myNavigation.pwm.set_pwm(myNavigation.drive_pwm_pin,0,0)
    time.sleep(2)
    '''
    
    myNavigation.Exit()
    sys.exit()

    #start gui
    myGui = gui.Display(myNavigation)
    my_queue = Queue.Queue()
    
    #initialize queue to default value so updateGuiPicture does not hang initially
    #default is 5 for stop sign
    my_queue.put(5)
    
    bufferedPipeThread = threading.Thread(target=myNavigation.GetSteeringAngleRotationTranslation,args=(my_queue,))
    '''
    Note: Threads can only .start() once, so create a new Thread each time for reading pipe
    '''
    
    #initialize startTime to current time plus 5 so the first attempt has 5 seconds to find a marker
    startTime = time.time() + 5
    MarkerTimeout = 1
    while not myNavigation.exitMain:
        if time.time() - startTime >= MarkerTimeout:
            my_queue.put(5) #put 5 for stop sign, immediately read by DisplayImageByNumber below so queue does not overflow
            if os.name == "posix":
                myNavigation.pwm.set_pwm(myNavigation.drive_pwm_pin,0,0)
        if not bufferedPipeThread.isAlive():
            bufferedPipeThread = threading.Thread(target=myNavigation.GetSteeringAngleRotationTranslation,args=(my_queue,))
            bufferedPipeThread.start()
            startTime = time.time()
            #bufferedPipeThread.join()
        
        #look into threading the navigation/buffered pipe or use unbuffered pipe from POpen
        
        if not my_queue.empty():
            myGui.DisplayImageByNumber(my_queue.get())
        
        #updateGui outside so GUI buttons work unconditionally
        myGui.updateGui()        
        
