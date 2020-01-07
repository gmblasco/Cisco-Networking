import requests
import json
import csv
import os
input_file = csv.DictReader(open('c:\Kibana\Vizualizations\Loopback2.csv'))
with open('c:\Kibana\Vizualizations\Create_Flow_monitor.json') as json_flow:
    flow = json.load(json_flow)
    json_flow_send = json.dumps(flow)
with open('c:\Kibana\Vizualizations\configure_flow_interface.json') as json_flow_int:
    flow_int = json.load(json_flow_int)
    json_flow_int_send = json.dumps(flow_int)
headers_flow = {
  'Accept': 'application/yang-data+json, application/yang-data.errors+json',
  'Content-Type': 'application/yang-data+json',
  'Authorization': 'Basic YWRtaW46WnhPcDM0ZWQ='
}
headers_interface = {
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
for raw in input_file:
    dep=raw['DEPENDENCIA']
    ip=raw['Loopback']
    url = "https://"+ip+":443/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet"
    urlnetflow = "https://"+ip+":443/restconf/data/Cisco-IOS-XE-native:native/flow"
    payload = ""
    host_up  = True if os.system("ping -n 1 " + ip) is 0 else False
    if host_up == 1:
        response = requests.request("GET", url, data=payload, headers=headers_interface, verify = False)
        data2 = json.loads(response.text) #guarda en dict el json
        fullpath=("E:\script\Cisco\Create interfaces via restconf\getint.json")
        with open(fullpath, 'w') as outfile:
            json.dump(data2, outfile)
        i=0
        for interface in data2["Cisco-IOS-XE-native:GigabitEthernet"]:
            if ('description' in data2["Cisco-IOS-XE-native:GigabitEthernet"][i].keys()and 'WAN' in data2["Cisco-IOS-XE-native:GigabitEthernet"][i]["description"]):
              print('La WAN en '+dep+ ' es la GigabitEhternet ' + data2["Cisco-IOS-XE-native:GigabitEthernet"][i]["name"])
              subint = data2["Cisco-IOS-XE-native:GigabitEthernet"][i]["name"]
              subintlist = list(subint)
              l = -1
              while True:
                  l = subint.find("/", l+1)
                  if l == -1:
                      break
                  print(l)
                  subintlist[l] = '%2F'
              subintfinal=''.join(subintlist)
              url_interface = "https://"+ip+":443/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet="+subintfinal+"/ip/flow"
              print('Borrando Netflow en ' + dep)
              response_delete = requests.request("DELETE", urlnetflow, headers=headers_flow, data = json_flow_send, verify = False)
              print(response_delete)
              print('Configurando Netflow en ' + dep)
              response_patch = requests.request("PATCH", urlnetflow, headers=headers_flow, data= json_flow_send, verify = False)
              print('Configurando Netflow en la interfaz ' + data2["Cisco-IOS-XE-native:GigabitEthernet"][i]["name"])
              print('accediendo a '+url_interface)
              response = requests.request("PATCH", url_interface, headers=headers_flow, data = json_flow_int_send, verify = False)
              url_save_config =  "https://"+ip+":443/restconf/operations/cisco-ia:save-config/"
              payload_save_config  = {}
              headers_save_config = {
                         'Accept': 'application/yang-data+json',
                         'Content-Type': 'application/yang-data+json',
                         'Authorization': 'Basic YWRtaW46WnhPcDM0ZWQ='
                        }
              response_save = requests.request("POST", url_save_config, headers=headers_save_config, data = payload_save_config, verify = False)
              print(response_save)
              i=i+1
            else:
              #print("boo")
              i=i+1
    else:
        print(dep +' host down')
        
