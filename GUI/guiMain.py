'''
Created on Sep 25, 2016

@author: Rahul
'''
#pip install Pillow
import PIL.Image
import PIL.ImageTk
import Tkinter


if __name__ == '__main__':

    root = Tkinter.Tk()
    textVar = "Click Me!!!"
    
    #load image and save it to variable
    upArrow = PIL.ImageTk.PhotoImage(PIL.Image.open("../resources/UpArrow.png"))
    downArrow = PIL.ImageTk.PhotoImage(PIL.Image.open("../resources/DownArrow.png"))
    rightArrow = PIL.ImageTk.PhotoImage(PIL.Image.open("../resources/RightArrow.png"))
    leftArrow = PIL.ImageTk.PhotoImage(PIL.Image.open("../resources/LeftArrow.png"))
    
    label = Tkinter.Label(root, image=upArrow)
    clickNumber = 2
    def onClick():
        #declare clickNumber as global so that clickNumber is actually incremented
        global clickNumber
        global upArrow
        global downArrow
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
    
    button = Tkinter.Button(root, text="I am a Butt, Touch me!", command = onClick)
    button.pack()
    label.pack()
    root.mainloop()