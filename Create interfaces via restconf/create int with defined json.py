import requests
import json
url = "https://172.31.99.45:443/restconf/data/Cisco-IOS-XE-native:native/interface/"
with open('c:\script\initest.json') as json_file:
    data = json.load(json_file)
jsonsend = json.dumps(data)
headers = {
    'Content-Type': "application/yang-data+json",
    'Authorization': "Basic YWRtaW46WnhPcDM0ZWQ=",
    'Accept': "application/yang-data+json, application/yang-data.errors+json",
    'cache-control': "no-cache",
    'Postman-Token': "18a4edd1-04ce-4189-b75c-22538756cdbc"
    }
with open('c:\script\json_viewing_error2.json', 'w') as fp:
    json.dump(data, fp)
    
#
#response = requests.request("POST", url, data=jsonsend, headers=headers, verify = False)

#print(response.text)
