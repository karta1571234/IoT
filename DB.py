# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 21:29:11 2021

@author: karta
"""


import pymysql as db

#connet DB

class DB:
    
    def __init__(self):
        self.connet_db=db.connect(host='localhost', user='root', password='', database='smart_home', charset='utf8') #連線資料庫
    
    def db_insert(self, temperature, gas, fire, water_Do, water_Ao, buzzer):
        
        with self.connet_db.cursor() as cursor:
            sql_insert="INSERT INTO `rpi_sensor` (`temperature`, `gas`, `fire`, `water_Do`, `water_Ao`, `buzzer`, `datetime`) VALUES (%s, %s, %s, %s, %s, %s, now())"
            cursor.execute(sql_insert,(temperature, gas, fire, water_Do, water_Ao, buzzer)) #執行SQL指令 回傳 1 表示執行 SQL 指令成功, 傳回一筆紀錄;0 表示新增成功 (但沒有傳回任何紀錄)
            
            """if exception:
                connet_db.rollback() #回滾
            """
            
            self.connet_db.commit()  #提交至DB 雖然回傳 1 表示 SQL 指令執行成功, 但所有更改資料庫的 SQL 操作結果只是實現於記憶體中, 需呼叫 Connection 物件的 commit() 方法才會真正寫入資料庫中
        
    def db_select(self):
        
        with self.connet_db.cursor() as cursor:
            sql_select="SELECT * FROM `rpi_sensor` WHERE 1"
            cursor.execute(sql_select)
            print(cursor.fetchall())
            
        
    def db_close(self):
        self.connet_db.close()   #關閉SQL連線