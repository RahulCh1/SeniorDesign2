'''
Created on Sep 28, 2016

@author: Rahul
'''
import os.path, sys
import Navigation
# Add current dir to search path.
sys.path.insert(0, "GUI")
# sys.path.insert(1, "Navigation")
import GuiDisplay as gui
#import Navigation

if __name__ == '__main__':
    
    #start navigation
    
    #start gui
    myGui = gui.Display()
    myGui.startGui()
    
    
    
        
        