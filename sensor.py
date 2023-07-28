# -*- coding: utf-8 -*-
"""
Created on Sat May 22 06:02:26 2021

@author: karta
"""

import time
import RPi.GPIO as GPIO
from w1thermsensor import W1ThermSensor
import random

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

Rled_Pin=35
Gled_Pin=37
R,G,B=11,13,15
Buzzer_Pin=21
Fire_Pin=33
Water_Pin=29

GPIO.setup(Rled_Pin,GPIO.OUT)   #Rled at 35 pin
GPIO.setup(Gled_Pin,GPIO.OUT)   #Gled at 37 pin
GPIO.setup(R,GPIO.OUT)          #Rpwm at 11 pin
GPIO.setup(G,GPIO.OUT)          #Gpwm at 13 pin
GPIO.setup(B,GPIO.OUT)          #Bpwm at 15 pin
GPIO.setup(Buzzer_Pin,GPIO.OUT) #Buzzer at 21 pin
GPIO.setup(Fire_Pin,GPIO.IN)    #Fire at 33 pin
GPIO.setup(Water_Pin, GPIO.IN)  #Water at 29 pin

Red = GPIO.PWM(Rled_Pin,500) #設定頻率為500Hz
Green = GPIO.PWM(Gled_Pin,500) 
Red.start(0)
Green.start(0)

pwmR = GPIO.PWM(R, 60)
pwmG = GPIO.PWM(G, 60)
pwmB = GPIO.PWM(B, 60)
pwmR.start(0)
pwmG.start(0)
pwmB.start(0)

Buzzer_PWM=GPIO.PWM(Buzzer_Pin,200)
Buzzer_PWM.start(0)

sensor = W1ThermSensor()
#part of temperature
while True:
    print("******************start******************")

    for dc in range(0, 101, 1): #dc: duty cycle
        Red.ChangeDutyCycle(dc)
        Green.ChangeDutyCycle(dc)
        time.sleep(0.015)
    for dc in range(100, -1, -1): #dc: duty cycle
        Red.ChangeDutyCycle(dc)
        Green.ChangeDutyCycle(dc)
        time.sleep(0.015)
        
    print("******************temperature******************")
    
    temperature = sensor.get_temperature()
    #C=float(temperature)
    C=random.randrange(16,40)       #for test
    if (C>30 and C<=35):
        pwmR.ChangeDutyCycle(100)
        print("******The temperature is high (%f C)******" %C)
        print("******The Red LED is on******")
    elif (C>25 and C<=30):
        pwmR.ChangeDutyCycle(100)
        pwmG.ChangeDutyCycle(100)
        print("******The temperture is normal (%f C)******" %C)
        print("******The Green LED and Red LED are on******")
    elif (C>18 and C<=25):
        pwmG.ChangeDutyCycle(100)
        print("******The temperture is comfortable (%f C)******" %C)
        print("******The Green LED is on******")
    else:
        print("******The temperture is unusual (maybe is so cold or so hot...) (%f C)******" %C)
        print("******Two lights are blinking******")
        
        i = 0
        while (i<=2):
            pwmR.ChangeDutyCycle(0)
            time.sleep(0.25)
            pwmG.ChangeDutyCycle(100)
            time.sleep(0.25)
            pwmG.ChangeDutyCycle(0)
            time.sleep(0.25)
            pwmR.ChangeDutyCycle(100)
            time.sleep(0.25)
            i+=1
        
    time.sleep(2)
    pwmR.ChangeDutyCycle(0)
    pwmG.ChangeDutyCycle(0)
    pwmB.ChangeDutyCycle(0)
    print("******************MQ-2******************")
    
#part of MQ-2 air detected sensor
        
    import smbus
    
    address = 0x48
    
    A0 = 0x40
    A1 = 0x41
    A2 = 0x42
    A3 = 0x43
    
    bus = smbus.SMBus(1)
  
#AO of MQ-2 input AIN3 of pcf-8591
    bus.write_byte(address,A3)                      #向PCF中寫入一個byte的資料
    bus.read_byte(address)                          #從PCF中讀取一個byte的資料
    air_value = bus.read_byte(address)
    bus.write_byte_data(address, A3, air_value)     #向PCF中寫入data
    print(f"********Current air_value is {air_value}********")
        
#part of buzzer alert  
    
    if(air_value>10):        #for test value is 10
        pwmR.ChangeDutyCycle(100)
        print("************** gas detected!! **************")
        for freq in range(200,801):
            Buzzer_PWM.ChangeFrequency(freq)   #freq為設置的新頻率 
            Buzzer_PWM.ChangeDutyCycle(50)     #Duty Cycle is 50 
            time.sleep(1.5/601)    #由200Hz到800需要1.5秒除上601個頻率=每個頻率要的時間
        for freq in range(800,199,-1):
            Buzzer_PWM.ChangeFrequency(freq)
            Buzzer_PWM.ChangeDutyCycle(50)
            time.sleep(3.5/601)
    else:
        pwmG.ChangeDutyCycle(100)
        print("************** Air Safe **************")
    Buzzer_PWM.ChangeDutyCycle(0)
    
    time.sleep(2)
    print("******************fire******************")
        
#part of fire detection
#檢測到火值為0沒有則為1
    fire_value=GPIO.input(Fire_Pin)
    print(f"********數字Do的值(有火為0無火為1)********")
    if(fire_value!=1):
        print(f"********Current fire_value is {fire_value}********")
        print("************ The Place is Fire! ************")
        
        i = 0
        while (i<=2):
            pwmR.ChangeDutyCycle(0)
            time.sleep(0.25)
            pwmG.ChangeDutyCycle(100)
            time.sleep(0.25)
            pwmG.ChangeDutyCycle(0)
            time.sleep(0.25)
            pwmR.ChangeDutyCycle(100)
            time.sleep(0.25)
            i+=1
            
        for freq in range(200,801):
            Buzzer_PWM.ChangeFrequency(freq)
            Buzzer_PWM.ChangeDutyCycle(50)     #Duty Cycle is 50 
            time.sleep(1.5/601)
        for freq in range(800,199,-1):
            Buzzer_PWM.ChangeFrequency(freq)
            Buzzer_PWM.ChangeDutyCycle(50)
            time.sleep(3.5/601)
    elif(fire_value==1):
        
        print(f"********Current fire_value is {fire_value}********")
        print("************ The Place is Safe! ************")
        
        for cdc in range(0,101):
            pwmR.ChangeDutyCycle(0)
            pwmG.ChangeDutyCycle(cdc)
            pwmB.ChangeDutyCycle(0)
            time.sleep(0.042)
        for cdc in range(100,-1,-1):
            pwmR.ChangeDutyCycle(0)
            pwmG.ChangeDutyCycle(cdc)
            pwmB.ChangeDutyCycle(0)
            time.sleep(0.042)  
        time.sleep(2)
        
    Buzzer_PWM.ChangeDutyCycle(0)
    pwmB.ChangeDutyCycle(0)
    pwmG.ChangeDutyCycle(0)

#part of water detection
#Do檢測到有雨值為0無雨則為1
#Ao值為0~255>>無雨~有雨
    water_TF_value=GPIO.input(Water_Pin)
    print(f"********數字Do的值(有雨為0無雨為1)********")
    print(f"********Current water_TF_value is {water_TF_value}********")
    
    if (water_TF_value!=1):
        print("************Raining************")
    elif (water_TF_value==1):
        print("************No raining************")
    time.sleep(0.5)

#Ao of water input AIN0 of pcf-8591
    bus.write_byte(address,A0)
    bus.read_byte(address)
    water_detail_value=bus.read_byte(address)
    bus.write_byte_data(address, A0, water_detail_value)
    print(f"******Current water_detail_value is {water_detail_value}******")
    if(water_detail_value<70):
        print(f"******The rain precipitaion is 100%******")
        while (i<=2):
            pwmR.ChangeDutyCycle(0)
            time.sleep(0.25)
            pwmG.ChangeDutyCycle(100)
            time.sleep(0.25)
            pwmG.ChangeDutyCycle(0)
            time.sleep(0.25)
            pwmR.ChangeDutyCycle(100)
            time.sleep(0.25)
            i+=1
    elif(water_detail_value>=70):
        water_Precipitation=100-(water_detail_value/2.55)       #(correction,normakiaztion)proportion is 100:255,Complementary
        print(f"******The rain precipitaion is {water_Precipitation}%******")
    time.sleep(2)
    
#part of RGB
    print("R")
    for cdc in range(0,101):
        pwmR.ChangeDutyCycle(cdc)
        pwmG.ChangeDutyCycle(0)
        pwmB.ChangeDutyCycle(0)
        time.sleep(0.015)
    for cdc in range(100,-1,-1):
        pwmR.ChangeDutyCycle(cdc)
        pwmG.ChangeDutyCycle(0)
        pwmB.ChangeDutyCycle(0)
        time.sleep(0.015)
    print("G")
    for cdc in range(0,101):
        pwmR.ChangeDutyCycle(0)
        pwmG.ChangeDutyCycle(cdc)
        pwmB.ChangeDutyCycle(0)
        time.sleep(0.015)
    for cdc in range(100,-1,-1):
        pwmR.ChangeDutyCycle(0)
        pwmG.ChangeDutyCycle(cdc)
        pwmB.ChangeDutyCycle(0)
        time.sleep(0.015)
    print("B")
    for cdc in range(0,100):
        pwmR.ChangeDutyCycle(0)
        pwmG.ChangeDutyCycle(0)
        pwmB.ChangeDutyCycle(cdc)
        time.sleep(0.015)
    for cdc in range(100,-1,-1):
        pwmR.ChangeDutyCycle(0)
        pwmG.ChangeDutyCycle(0)
        pwmB.ChangeDutyCycle(cdc)
        time.sleep(0.015)

    print("******************end********************")
    
    time.sleep(2)