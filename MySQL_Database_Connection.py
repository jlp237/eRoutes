#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 15 12:32:53 2018

@author: vancura
"""

# USER and PASSWORD need to be replaced


# importing mysql connector package

import mysql.connector    

# connection to HTW Mobility MySQL - DB and preset electric_vehicles as database

connection = mysql.connector.connect(user='USER', password='PASSWORD',
                              host='mobility.f4.htw-berlin.de',
                              database='electric_vehicles')

# try / finally for potential erros in SQL queries

try:
   cursor = connection.cursor()
   cursor.execute("SELECT * FROM vehicle_specs")
   
   # for-loop with cursor through all cars in table vehicle_specs

   for (id, manufacturer, type) in cursor:
       print("Auto Nr. " + str(id) + " ist von " + manufacturer + " und nennt sich " + type)
       
finally:
    connection.close()