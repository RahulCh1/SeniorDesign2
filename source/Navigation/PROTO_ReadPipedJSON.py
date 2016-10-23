#source: http://stackoverflow.com/questions/36748829/piping-binary-data-between-python-and-c
import subprocess
import json


if __name__ == '__main__':
    '''
    subprocess.Popen opens out.exe (the C++ program)
    
    stdin of out.exe is piped and controlled by python
    stdout of out.exe is piped and read by python
    '''
    
    proc = subprocess.Popen("C:/Users/Rahul/Desktop/ArUCO/SeniorDesign2ArUCO/build/bin/Release/aruco_simple.exe",cwd=r'C:/Users/Rahul/Desktop/ArUCO/SeniorDesign2ArUCO/build/bin/Release/',stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    # Replace path to SeniorDesign2ArUCO folder below. ALSO replace path in option cwd=r'<PATH TO SeniorDesign2ArUCO>/...'
    #pathToArUCO = "<PATH TO SeniorDesign2ArUCO>";
    #proc = subprocess.Popen(pathToArUCO + "/SeniorDesign2ArUCO/build/bin/Release/aruco_simple.exe",cwd=r'<PATH TO SeniorDesign2ArUCO>/SeniorDesign2ArUCO/build/bin/Release/',stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    
    '''
    It works! The C program was hanging on imread("../../resources/leftArrow.png") because the 
    current working directory was not set as where the executable is being called from.
    Fixed by setting cwd (current working directory) in Popen
    source: http://stackoverflow.com/questions/1685157/python-specify-popen-working-directory-via-argument
    '''
    
    while True:
        message = proc.stdout.readline()
        message = message.strip() #remove blanks
        if message != '':
            #print str(i) +": " + message
        
            parsed_json = json.loads(message)
        
        print(str(parsed_json["Markers"][0]["ID"]) + ":  " + str(parsed_json["Markers"][0]["T"]["y"]) + "\n    " + str(parsed_json["Markers"][0]["R"]["y"]) + "\n")
    
    '''
    Popen.wait() waits for the child process to terminate
    Popen.kill() kills the child process
    '''
    proc.kill()