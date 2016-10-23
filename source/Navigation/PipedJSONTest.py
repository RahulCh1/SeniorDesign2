# source: http://stackoverflow.com/questions/2835559/parsing-values-from-a-json-file-in-python
import unittest
from PipedJSON import PipedJSON
import json
import time

class Test(unittest.TestCase):

    def test_parseJSON(self):
                
        jsonText = "{ \"Markers\": [{ \"ID\": 8, \"T\": { \"x\": -0.057926, \"y\": 0.012215, \"z\": 0.410324}}] }"
        
        parsed_json = json.loads(jsonText)
        
        self.assertEqual(str(parsed_json["Markers"][0]["ID"]),"8", "Detected marker" + str(parsed_json["Markers"][0]["ID"]))
    
    def test_OpenCamera(self):
        pipedTest = PipedJSON("aruco_simple.exe","C:/Users/Rahul/Desktop/ArUCO/SeniorDesign2ArUCO/build/bin/Release")
        time.sleep(1)
        pipedTest.KillProcess()
        time.sleep(1)
        
    '''
    Must test with ArUCO marker in front of the camera
    '''
    def test_PipedJSON(self):
        pipedTest = PipedJSON("aruco_simple.exe","C:/Users/Rahul/Desktop/ArUCO/SeniorDesign2ArUCO/build/bin/Release")
        
        i = 0
        while i<10:
            
            # GetParsedJSON() is a blocking method
            parsed_json = pipedTest.GetParsedJSON()
            
            print "Marker ID is: " + str(parsed_json["Markers"][0]["ID"])
            print "Translation X is: " + str(parsed_json["Markers"][0]["T"]["x"]) + "\n"
            i += 1
        
        pipedTest.KillProcess()
    
    
    
    if __name__ == '__main__':
        unittest.main()

    
    
# source: http://stackoverflow.com/questions/2835559/parsing-values-from-a-json-file-in-python

import json

if __name__ == '__main__':
    jsonText = "{ \"Markers\": [{ \"ID\": 8, \"T\": { \"x\": -0.057926, \"y\": 0.012215, \"z\": 0.410324}}] }"
    
    parsed_json = json.loads(jsonText)
    
#     with open('data.json') as thingy:
#         parsed_json = json.load(thingy)
        
    print(parsed_json["Markers"][0]["ID"])
    
    