'''
Created on Sep 28, 2016

@author: Rahul
'''
import os.path, sys

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
    
    while True:
        #look into threading the GUI or use unbuffered pipe from POpen
        myGui.updateGui()
        myGui.DisplayImageByNumber(myNavigation.GetSteeringAngleRotationTranslation())
    
    
    
        
        