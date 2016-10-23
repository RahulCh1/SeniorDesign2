'''
Created on Sep 28, 2016

@author: Rahul
'''
#pip install Pillow
import PIL.Image
import PIL.ImageTk
import Tkinter
from Navigation import Navigation
'''
 RC - used globals to make this work because did not want to self.var name each time.
 I will look up better practice for this 
'''

class Display(object):
    '''
    classdocs
    '''    
    
    def __init__(self,myNavigation):
        '''
        Constructor
        '''
        global upArrow
        global downArrow
        global rightArrow
        global leftArrow
        global Stop1
        global Stop2
        global Stop3
        global Stop4
        global Stop
        global label
        global clickNumber
        
        #must create Tk() object before using ImageTk to open image
        self.root = Tkinter.Tk()
        self.root.geometry('{}x{}'.format(300, 400))
        
        #load image and save it to variable
        upArrow = PIL.ImageTk.PhotoImage(PIL.Image.open("../resources/UpArrow.png"))
        downArrow = PIL.ImageTk.PhotoImage(PIL.Image.open("../resources/DownArrow.png"))
        rightArrow = PIL.ImageTk.PhotoImage(PIL.Image.open("../resources/RightArrow.png"))
        leftArrow = PIL.ImageTk.PhotoImage(PIL.Image.open("../resources/LeftArrow.png"))
        Stop = PIL.ImageTk.PhotoImage(PIL.Image.open("../resources/Stop.png"))
        Stop1 = PIL.ImageTk.PhotoImage(PIL.Image.open("../resources/Stop1.jpg"))
        Stop2 = PIL.ImageTk.PhotoImage(PIL.Image.open("../resources/Stop2.jpg"))
        Stop3 = PIL.ImageTk.PhotoImage(PIL.Image.open("../resources/Stop3.jpg"))
        Stop4 = PIL.ImageTk.PhotoImage(PIL.Image.open("../resources/Stop4.jpg"))
        
        label = Tkinter.Label(self.root, image=upArrow)
        clickNumber = 0
        button = Tkinter.Button(self.root, text="Simulate Being Called!", command = lambda: self.onClick())
        exitButton = Tkinter.Button(self.root, text="Exit", command = lambda: myNavigation.Exit())
        button.pack()
        exitButton.pack()
        label.pack()
    
    def startGuiMainLoop(self):
        self.root.mainloop()
        
    def updateGui(self):
        self.root.update()
            
    def onClick(self):
        #declare clickNumber as global so that clickNumber is actually incremented
        global upArrow
        global downArrow
        global leftArrow
        global rightArrow
        global clickNumber
        global label
        
        clickNumber += 1
        self.DisplayImageByNumber(clickNumber)
        print clickNumber
#         if clickNumber % 4 == 0 :
#             label.configure(image = rightArrow)
#             label.image = rightArrow
#         elif clickNumber % 3 == 0 :
#             label.configure(image = downArrow)
#             label.image = downArrow
#         elif clickNumber % 2 == 0:
#             label.configure(image = leftArrow)
#             label.image = leftArrow
#         else:
#             label.configure(image = upArrow)
#             label.image = upArrow
        if clickNumber >= 9 :
            clickNumber = 0
        
            
    def DisplayImageByNumber(self,ImageNumber):
        #declare clickNumber as global so that clickNumber is actually incremented
        global upArrow
        global downArrow
        global leftArrow
        global rightArrow
        global Stop1
        global Stop2
        global Stop3
        global Stop4
        global Stop
        global label
        
        if ImageNumber == 1 :
            label.configure(image = Stop1)
            label.image = Stop1
        elif ImageNumber == 2 :
            label.configure(image = Stop2)
            label.image = Stop2
        elif ImageNumber == 3:
            label.configure(image = Stop3)
            label.image = Stop3
        elif ImageNumber == 4:
            label.configure(image = Stop4)
            label.image = Stop4
        elif ImageNumber ==  5:
            label.configure(image = Stop)
            label.image = Stop
        elif ImageNumber == 7 :
            label.configure(image = rightArrow)
            label.image = rightArrow
        elif ImageNumber == 8 :
            label.configure(image = downArrow)
            label.image = downArrow
        elif ImageNumber == 9:
            label.configure(image = leftArrow)
            label.image = leftArrow
        elif ImageNumber == 6:
            label.configure(image = upArrow)
            label.image = upArrow
        
    