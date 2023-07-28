# -*- coding: utf-8 -*-
"""
Created on Sun Dec 19 17:00:31 2021

@author: karta
"""


import RPi.GPIO as GPIO
from w1thermsensor import W1ThermSensor
#import random
import smbus

class IoT:
    
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        
        #Buzzer_Pin=21
        self.Fire_Pin=33
        self.Water_Pin=29

        #GPIO.setup(Buzzer_Pin,GPIO.OUT) #Buzzer at 21 pin
        GPIO.setup(self.Fire_Pin,GPIO.IN)    #Fire at 33 pin
        GPIO.setup(self.Water_Pin, GPIO.IN)  #Water at 29 pin

        #setup pcf-8591
        self.address = 0x48
        
        self.A0 = 0x40
        self.A1 = 0x41
        self.A2 = 0x42
        self.A3 = 0x43
        
        self.bus = smbus.SMBus(1)
      
        
#part of temperature
    def gett_temperature(self):
        print("******************temperature******************")
        
        sensor = W1ThermSensor()  
        temperature = sensor.get_temperature()
        
        C=float(temperature)
        #C=random.randrange(16,40)       #for test
        if (C>30 and C<=35):
            print("******The temperature is high (%f C)******" %C)
        elif (C>25 and C<=30):
            print("******The temperture is normal (%f C)******" %C)
        elif (C>18 and C<=25):
            print("******The temperture is comfortable (%f C)******" %C)
        else:
            print("******The temperture is unusual (maybe is so cold or so hot...) (%f C)******" %C)
        
        return C
        
#part of MQ-2 air detected sensor        
    def get_gas(self):
        print("******************MQ-2******************") 

        #AO of MQ-2 input AIN3 of pcf-8591
        self.bus.write_byte(self.address,self.A3)                      #向PCF中寫入一個byte的資料
        self.bus.read_byte(self.address)                          #從PCF中讀取一個byte的資料
        air_value = self.bus.read_byte(self.address)
        self.bus.write_byte_data(self.address, self.A3, air_value)     #向PCF中寫入data
        print(f"********Current air_value is {air_value}********")
        
        if(air_value>20):        #for test value is 20
            print("************** gas detected!! **************")
        else:
            print("************** Air Safe **************")
        
        return air_value
        
#part of fire detection
#檢測到火值為0沒有則為1    
    def get_fire(self):
        print("******************fire******************")
        fire_value=GPIO.input(self.Fire_Pin)
        print(f"********數字Do的值(有火為0無火為1)********")
        if(fire_value!=1):
            print(f"********Current fire_value is {fire_value}********")
            print("************ The Place is Fire! ************")
        elif(fire_value==1):  
            print(f"********Current fire_value is {fire_value}********")
            print("************ The Place is Safe! ************")
            
        return fire_value
#part of water detection
#Do檢測到有雨值為0無雨則為1
#Ao值為0~255>>無雨~有雨
    def get_water_Do(self):
        print("******************water******************")
        water_TF_value=GPIO.input(self.Water_Pin)
        print(f"********數字Do的值(有雨為0無雨為1)********")
        print(f"********Current water_TF_value is {water_TF_value}********")
        if (water_TF_value!=1):
            print("************Raining************")
        elif (water_TF_value==1):
            print("************No raining************")
        return water_TF_value

    def get_water_Ao(self):
        #Ao of water input AIN0 of pcf-8591
        self.bus.write_byte(self.address,self.A0)
        self.bus.read_byte(self.address)
        water_detail_value=self.bus.read_byte(self.address)
        self.bus.write_byte_data(self.address, self.A0, water_detail_value)
        print(f"******Current water_detail_value is {water_detail_value}******")
        if(water_detail_value<70):
            print(f"******The rain precipitaion is 100%******")
            return 100
        elif(water_detail_value>=70):
            water_Precipitation=100-(water_detail_value/2.55)       #(correction,normakiaztion)proportion is 100:255,Complementary
            print(f"******The rain precipitaion is {water_Precipitation}%******")
            return water_Precipitation
        
    print("******************start******************")
