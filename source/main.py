'''
Created on Sep 28, 2016

@author: Rahul
'''
import os.path, sys
# Add current dir to search path.
sys.path.insert(0, "GUI")

import GuiDisplay as gui

if __name__ == '__main__':
    myGui = gui.Display()
    myGui.startGui()