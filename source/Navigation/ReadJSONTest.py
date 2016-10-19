# source: http://stackoverflow.com/questions/2835559/parsing-values-from-a-json-file-in-python

import json

if __name__ == '__main__':
    jsonText = "{ \"Markers\": [{ \"ID\": 8, \"T\": { \"x\": -0.057926, \"y\": 0.012215, \"z\": 0.410324}}] }"
    
    parsed_json = json.loads(jsonText)
    
#     with open('data.json') as thingy:
#         parsed_json = json.load(thingy)
        
    print(parsed_json["Markers"][0]["ID"])
    
    