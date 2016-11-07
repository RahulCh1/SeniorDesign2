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

    '''
    myNavigation.Forward()
    time.sleep(2.5)
    myNavigation.TurnLeft(1.5)
    
    myNavigation.Steer(myNavigation.servo_middle)
	
    myNavigation.Exit()
    sys.exit()
    '''
    
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
                myNavigation.Stop()
                #print "Stopping drive motor!"
        if not bufferedPipeThread.isAlive():
            bufferedPipeThread = threading.Thread(target=myNavigation.GetSteeringAngleRotationTranslation,args=(my_queue,))
            bufferedPipeThread.start()
            startTime = time.time()
            #bufferedPipeThread.join()
        
        #look into threading the navigation/buffered pipe or use unbuffered pipe from POpen
        
        if not my_queue.empty():
            markerID = my_queue.get()
            myGui.DisplayImageByNumber(markerID)
        
        #updateGui outside so GUI buttons work unconditionally
        myGui.updateGui()        
        
