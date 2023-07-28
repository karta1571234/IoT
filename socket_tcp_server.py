# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 14:42:03 2021

@author: karta
"""


import socket
import ssl
from IoT import IoT
import time


hostname = '192.168.0.116'
port = 5288 
addr = (hostname,port)

count=1
#[Header, Command, Sequence, Reserved, Temp, gas, fire, w_Do, w_Ao, buzzer, CC]
sensor_values_bytes=bytearray([0x88, 0x1B, 0x01, 0x00, ])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = ssl.wrap_socket(sock=server, keyfile='./privkey.pem', certfile='./certificate.pem', server_side=True)  #對比沒有加密的通信，其實加密通信就是利用ssl.wrap_socket將創建的socket包起來而已，運行結果一致。
server.bind(addr)
server.listen(2)
server.settimeout(5)

print("waitting connect...")

IoT = IoT() #new class

while True:
    try:
        connect_socket,client_addr = server.accept()
        print("Client address:",client_addr)
        
        if count==1:
            print("client connect success!!")
            connect_socket.send(bytes("Hi, here are Rpi server.",encoding='utf-8'))
            count-=1
            
    except KeyboardInterrupt:
        server.close()
        print("KeyboardInterrupt. server close~")
        print("pressed Ctrl+c. server close~")
        break
    except ConnectionResetError:
        server.close()
        print("ConnectionResetError. server close~")
        print("Client stop so server close~")
        break
    except socket.timeout:
        server.close()
        print("Server timeout~")
        break
    else:
        #數值
        temperature=int(IoT.gett_temperature())#溫度
        temp_units_digit=temperature%10 #個位數
        temp_tens_digit=temperature-temp_units_digit #十位數
        
        gas=IoT.get_gas()#瓦斯MQ-2
        fire=IoT.get_fire()#火源
        water_Do=IoT.get_water_Do()#雨水數位
        water_Ao=int(IoT.get_water_Ao())#雨水類比
        if gas>8 or fire==0 or water_Do==0:
            buzzer=1
        else:
            buzzer=0
        
        CC=temp_units_digit^temp_tens_digit #check code=temperature^
        
        #將數值裝成array一次傳送
        sensor_values_bytes.append(temp_tens_digit)
        sensor_values_bytes.append(temp_units_digit)
        
        sensor_values_bytes.append(gas)
        sensor_values_bytes.append(fire)
        sensor_values_bytes.append(water_Do)
        sensor_values_bytes.append(water_Ao)
        sensor_values_bytes.append(buzzer)
        
        sensor_values_bytes.append(CC)
        
        #connect_socket.send(str(temperature).encode('utf8'))
        connect_socket.send(sensor_values_bytes)
        print("send:",sensor_values_bytes)
        
        del sensor_values_bytes[4:12]   #清空array
        #接收client給server確認的值
        check_sensor_values=bytearray(connect_socket.recv(1024))
        print("check:",check_sensor_values)
        
        time.sleep(1)