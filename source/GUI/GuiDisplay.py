'''
Created on Sep 28, 2016

@author: Rahul
'''
#pip install Pillow
import PIL.Image
import PIL.ImageTk
import Tkinter

'''
 RC - used globals to make this work because did not want to self.var name each time.
 I will look up better practice for this 
'''

class Display(object):
    '''
    classdocs
    '''    
    
    def __init__(self):
        '''
        Constructor
        '''
        global upArrow
        global downArrow
        global rightArrow
        global leftArrow
        global label
        global clickNumber
        
        #must create Tk() object before using ImageTk to open image
        self.root = Tkinter.Tk()
        
        #load image and save it to variable
        upArrow = PIL.ImageTk.PhotoImage(PIL.Image.open("../resources/UpArrow.png"))
        downArrow = PIL.ImageTk.PhotoImage(PIL.Image.open("../resources/DownArrow.png"))
        rightArrow = PIL.ImageTk.PhotoImage(PIL.Image.open("../resources/RightArrow.png"))
        leftArrow = PIL.ImageTk.PhotoImage(PIL.Image.open("../resources/LeftArrow.png"))
        
        
        label = Tkinter.Label(self.root, image=upArrow)
        clickNumber = 1
        button = Tkinter.Button(self.root, text="I am a Butt, Touch me!", command = lambda: self.onClick())
        button.pack()
        label.pack()
    
    def startGui(self):
        self.root.mainloop()
            
    def onClick(self):
        #declare clickNumber as global so that clickNumber is actually incremented
        global upArrow
        global downArrow
        global leftArrow
        global rightArrow
        global clickNumber
        global label
        
        clickNumber += 1
        print clickNumber
        if clickNumber % 4 == 0 :
            label.configure(image = rightArrow)
            label.image = rightArrow
        elif clickNumber % 3 == 0 :
            label.configure(image = downArrow)
            label.image = downArrow
        elif clickNumber % 2 == 0:
            label.configure(image = leftArrow)
            label.image = leftArrow
        else:
            label.configure(image = upArrow)
            label.image = upArrow
        if clickNumber > 4 :
            clickNumber = 1
    