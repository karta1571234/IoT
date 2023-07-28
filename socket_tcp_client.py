# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 14:44:20 2021

@author: karta
"""


import socket
import ssl
import time
from DB import DB

#client-server connect
hostname = '192.168.0.116'
port = 5288
addr = (hostname,port)

count=1

"""
socket.AF_INET: IPv4 (Default)
socket.SOCK_STREAM: TCP (Default) 
socket.SOCK_DGRAM: UDP
"""

db = DB()   #new DB class

while True:
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        client = ssl.wrap_socket(sock=client, keyfile='./privkey.pem', certfile='./certificate.pem',server_side=False)
        client.connect(addr)
        
        if count==1:
            server_respose = str(client.recv(1024), encoding='utf-8')
            print("server connect success!!")
            print('Server start:', server_respose)
            count-=1
        
    except KeyboardInterrupt:
        client.close()
        print("KeyboardInterrupt. client close~")
        print("pressed Ctrl+c. client close~")
        break
    except ConnectionRefusedError:
        client.close()
        print("ConnectionRefusedError. client close~")
        print("Server stop so client close~")
        break
    except ConnectionResetError:
        client.close()
        print("ConnectionRefusedError. client close~")
        print("Server stop so client close~")
        break
    else:
        #temperature = int(client.recv(1024).decode('utf8'))
        #print("temperature:",temperature)
        
        sensor_values = bytearray(client.recv(1024))
        print("sensor_values:",sensor_values)
        
        if sensor_values[4]^sensor_values[5]==sensor_values[11]:    #做XOR檢查
            print("Check Code OK.")
            print(type(sensor_values))
            #connect DB and INSERT values.    
            db.db_insert((sensor_values[4]+sensor_values[5]), sensor_values[6], sensor_values[7], 
                         sensor_values[8], sensor_values[9], sensor_values[10])
            print("DATA INSERT OK.")
        else:
            print(f"Check Code Not OK. CC:{sensor_values[11]}")
        
        #收到的值再回傳給server確認
        client.send(sensor_values)
        
        time.sleep(1)
        
db.db_close()