import requests
import json

url = "https://172.31.99.23:443/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet"

payload = ""
headers = {
    'Accept': "application/yang-data+json",
    'Authorization': "Basic YWRtaW46WnhPcDM0ZWQ=",
    'User-Agent': "PostmanRuntime/7.19.0",
    'Cache-Control': "no-cache",
    'Postman-Token': "82bb1ad9-c8fc-4344-bd65-e5a114828831,53c6d31e-6d93-4c25-b5fc-a7eb85a0a1e7",
    'Host': "172.31.99.45:443",
    'Accept-Encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

response = requests.request("GET", url, data=payload, headers=headers, verify = False)

print(response.text)
data2 = json.loads(response.text) #guarda en dict el json
fullpath=("E:\script\Cisco\Create interfaces via restconf\getint.json")
with open(fullpath, 'w') as outfile:
    json.dump(data2, outfile)
i=0
for interface in data2["Cisco-IOS-XE-native:GigabitEthernet"]:
    if ('description' in data2["Cisco-IOS-XE-native:GigabitEthernet"][i].keys()and 'WAN' in data2["Cisco-IOS-XE-native:GigabitEthernet"][i]["description"]):
      print('La WAN es' + ' ' + data2["Cisco-IOS-XE-native:GigabitEthernet"][i]["name"])
      i=i+1
    else:
      print("boo")
      i=i+1
