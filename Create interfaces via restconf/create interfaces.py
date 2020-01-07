import json
import ipaddress
with open('c:\script\inicializador.json') as json_file:
    data = json.load(json_file)
    #for p in data['Cisco-IOS-XE-native:GigabitEthernet']:
     #   print('Name: ' + p['name'])
      #  print(p['ip']['address'])
print('Ingrese la IP de loopback del router a configurar')
loopback = input()
while True:
    try:
        ipaddress.ip_address(loopback)
    except ValueError:
        print('La ip ingresada es incorrecta')
        print('Ingrese la IP de loopback del router a configurar')
        loopback = input()
    else:
        break
uri = ('https://'+loopback+':443/restconf/data/Cisco-IOS-XE-native:native/interface/')
print('Desea configurar una interfaz GigabitEthernet para este dispositivo Y/N?')
respuesta = input()
respuesta = respuesta.upper()
if respuesta == ('Y'):
    print('ingrese la interfaz o subinterfaz Gi a configurar ej: 0/0/1.180')
    interface = input()
    if '.' in interface:
        print('Ingrese el vlan id de la interfaz a configurar:')
        vlan = input()
        break
   
    print('Ingrese la dirección IP de la interfaz a configurar')
    ip = input()
    while True:
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            print('La ip ingresada es incorrecta')
            print('Ingrese la IP nuevamente')
            ip = input()
        else:
            break
    mask= input()
    
else:
    exit()
