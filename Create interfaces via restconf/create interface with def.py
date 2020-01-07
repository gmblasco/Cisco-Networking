import json
import ipaddress
import socket
import struct
import http.client
import requests
def valid_ip(a):
    #Funcion para validar que una ip sea válida
    while True:
        try:
            ipaddress.ip_address(a)	
        except ValueError:
            #si no es válida pide ingrsarla hasta que lo sea
            print('La ip ingresada es incorrecta')
            print('Ingrese la IP nuevamente')
            a = input()
        else:
            break
        #devuelve la ip válidada
    return a
def cidr(prefix):
    return socket.inet_ntoa(struct.pack(">I", (0xffffffff << (32 - prefix)) & 0xffffffff))

with open('c:\script\inicializador.json') as json_file:
    data = json.load(json_file)
    #for p in data['Cisco-IOS-XE-native:GigabitEthernet']:
     #   print('Name: ' + p['name'])
      #  print(p['ip']['address'])
print('Ingrese la IP de loopback del router a configurar')
loopback = input()
loopback = valid_ip(loopback)
uri = ('https://'+loopback+':443/restconf/data/Cisco-IOS-XE-native:native/interface/')
print('Desea configurar una interfaz GigabitEthernet para este dispositivo Y/N?')
respuesta = input()
respuesta = respuesta.upper()
i=0
while respuesta == ('Y'):
    print('ingrese la interfaz o subinterfaz Gi a configurar ej: 0/0/1.180')
    interface = input()
    if '.' in interface:
        print('Ingrese el vlan id de la interfaz a configurar:')
        vlan = input()
           
    print('Ingrese la dirección IP de la interfaz a configurar')
    ip = input()
    ip = valid_ip(ip)
    print('Ingrese Máscara de Subred en formato CIDR: Ej para /24 ingresar 24')
    mask = input()
    maskint = int(mask)
    mask = cidr(maskint)
    print('Ingrese la descripción de la interfaz')
    description = input()
    if i==0:
        data['Cisco-IOS-XE-native:GigabitEthernet'][i]['name'] = interface
        data['Cisco-IOS-XE-native:GigabitEthernet'][i]['encapsulation']['dot1Q']['vlan-id'] = int(vlan)
        data['Cisco-IOS-XE-native:GigabitEthernet'][i]['ip']['address']['primary']['address'] = ip
        data['Cisco-IOS-XE-native:GigabitEthernet'][i]['ip']['address']['primary']['mask'] = mask
        data['Cisco-IOS-XE-native:GigabitEthernet'][i]['description'] = description
        i = i+1
        print('Desea configurar otra interfaz GigabitEthernet para este dispositivo Y/N?') 
        respuesta = input()
        respuesta = respuesta.upper()
    else:
        addtolist=data['Cisco-IOS-XE-native:GigabitEthernet']
        addtolist[0]['name'] = '"'+interface+'"'
        addtolist[0]['encapsulation']['dot1Q']['vlan-id'] = int(vlan)
        addtolist[0]['ip']['address']['primary']['address'] = ip
        addtolist[0]['ip']['address']['primary']['mask'] = mask
        addtolist[0]['description'] = description
        data['Cisco-IOS-XE-native:GigabitEthernet'].append(addtolist[0])
        i = i+1
        print('Desea configurar otra interfaz GigabitEthernet para este dispositivo Y/N?') 
        respuesta = input()
        respuesta = respuesta.upper()
headers = {
    'Content-Type': "application/yang-data+json",
    'Authorization': "Basic YWRtaW46WnhPcDM0ZWQ=",
    'Accept': "application/yang-data+json, application/yang-data.errors+json",
    'cache-control': "no-cache",
    'Postman-Token': "18a4edd1-04ce-4189-b75c-22538756cdbc"
    }
with open('c:\script\json_viewing_error.json', 'w') as fp:
    json.dump(data, fp)
with open('c:\script\json_viewing_error.json') as fp:    
    data = json.load(fp)
senddata = json.dumps(data)
    
response = requests.request("POST", uri, data=senddata, headers=headers, verify = False)

print(response.text)   


