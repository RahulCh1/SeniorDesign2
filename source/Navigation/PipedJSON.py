'''
Created on Oct 20, 2016

@author: Rahul
'''
#source: http://stackoverflow.com/questions/36748829/piping-binary-data-between-python-and-c

import subprocess
import json

class PipedJSON(object):
    '''
    classdocs
    '''

    
    def __init__(self, executableName, directoryToExecutable):
        '''
        subprocess.Popen opens out.exe (the C++ program)
        
        stdin of out.exe is piped and controlled by python
        stdout of out.exe is piped and read by python
        '''
        try:
            self.process = PProcess(executableName,directoryToExecutable)
        except:
            print "Error opening executable in PipedJSON.py!"
            self.KillProcess()
        
    '''
    Blocking method
    Returns JSON containing JSON info from C++ OpenCV
    '''    
    def GetParsedJSON(self):
        return json.loads(self.ReadRawJSON())

    
    def ReadRawJSON(self):
        return self.process.openedProcess.stdout.readline().strip() #remove blanks
    
    '''
    Untested, maybe unnecessary
    '''
    def SendMessageToC(self,str):
        self.process.openedProcess.stdin.write(str)
    
    def KillProcess(self):
        self.process.KillProcess()
        
        
class PProcess(object):
    
    
    def __init__(self, executableName, directoryToExecutable):
        '''
        subprocess.Popen opens out.exe (the C++ program)
        
        stdin of out.exe is piped and controlled by python
        stdout of out.exe is piped and read by python
        '''
                
        '''
        It works! The C program was hanging on imread("../../resources/leftArrow.png") because the 
        current working directory was not set as where the executable is being called from.
        Fixed by setting cwd (current working directory) in Popen
        source: http://stackoverflow.com/questions/1685157/python-specify-popen-working-directory-via-argument
        '''
        self.openedProcess = subprocess.Popen(directoryToExecutable + "/" + executableName,cwd=directoryToExecutable,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        
    '''
    Popen.wait() waits for the child process to terminate
    Popen.kill() kills the child process
    '''      
    def KillProcess(self):
        self.openedProcess.kill()
    
        