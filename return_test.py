# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 23:36:07 2021

@author: karta
"""

import time
from IoT import IoT

I = IoT()
while 1:
    temp=I.gett_temperature()
    gas=I.get_gas()
    fire=I.get_fire()
    water_Do=I.get_water_Do()
    water_Ao=I.get_water_Ao()
    if gas>8 or fire==0 or water_Do==0:
        buzzer=1
    else:
        buzzer=0
    
    print("value:",temp)
    print("value:",gas)
    print("value:",fire)
    print("value_Do:",water_Do)
    print("value_Ao:",water_Ao)
    print("buzzer:",buzzer)
    
    time.sleep(1)