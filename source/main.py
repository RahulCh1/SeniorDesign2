'''
Created on Sep 28, 2016

@author: Rahul
'''
import os.path, sys
import threading 
import Queue
# Add current dir to search path.
sys.path.insert(0, "GUI")
# sys.path.insert(1, "Navigation")

import GuiDisplay as gui

from Navigation import Navigation

if __name__ == '__main__':
    
    #start navigation
    myNavigation = Navigation()
    
    #start gui
    myGui = gui.Display(myNavigation)
    my_queue = Queue.Queue()
    
    #initialize queue to default value so updateGuiPicture does not hang initially
    #default is 5 for stop sign
    my_queue.put(5)
    
    bufferedPipeThread = threading.Thread(target=myNavigation.GetSteeringAngleRotationTranslation,args=(my_queue,))
    
    # Threads can only .start() once, so create a new Thread each time for reading pipe
    while not myNavigation.exitMain:
            
        if not bufferedPipeThread.isAlive():
            bufferedPipeThread = threading.Thread(target=myNavigation.GetSteeringAngleRotationTranslation,args=(my_queue,))
            bufferedPipeThread.start()
#         bufferedPipeThread.join()
        
        #look into threading the navigation/buffered pipe or use unbuffered pipe from POpen
        
        if not my_queue.empty():
            myGui.DisplayImageByNumber(my_queue.get())
        
        #updateGui outside so GUI buttons work unconditionally
        myGui.updateGui()    
    
    
    
        
        