import requests
import json
import csv
import os
input_file = csv.DictReader(open('c:\Kibana\Vizualizations\Loopback3.csv'))
with open('e:\script\Cisco\domainlookup\srcip.json') as json_flow:
    flow = json.load(json_flow)
    json_flow_send = json.dumps(flow)
headers_flow = {
  'Accept': 'application/yang-data+json, application/yang-data.errors+json',
  'Content-Type': 'application/yang-data+json',
  'Authorization': 'Basic YWRtaW46WnhPcDM0ZWQ='
}
for raw in input_file:
    dep=raw['DEPENDENCIA']
    ip=raw['Loopback']
    url = "https://"+ip+":443/restconf/data/Cisco-IOS-XE-native:native"
    payload = ""
    url_save_config =  "https://"+ip+":443/restconf/operations/cisco-ia:save-config/"
    payload_save_config  = {}
    headers_save_config = {
                          'Accept': 'application/yang-data+json',
                          'Content-Type': 'application/yang-data+json',
                          'Authorization': 'Basic YWRtaW46WnhPcDM0ZWQ='
                          }
    host_up  = True if os.system("ping -n 1 " + ip) is 0 else False
    if host_up == 1:
        print('configuring ' +dep+ ' ip domain lookup and ssh source interface')
        response_patch = requests.request("PATCH", url, headers=headers_flow, data= json_flow_send, verify = False)
        print('saving ' +dep+ ' configuration to startup config')
        response_save = requests.request("POST", url_save_config, headers=headers_save_config, data = payload_save_config, verify = False)
    else:
        print(dep +' host down')
        
