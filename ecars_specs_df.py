# -*- coding: utf-8 -*-
"""
Created on Sun May  6 12:37:15 2018

@author: Jan-Lukas, David, Tobias
"""

import mysql.connector
import requests
from bs4 import BeautifulSoup
   

url = 'https://ev-database.uk'
resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'lxml')

urls = []
cars = []
for h in soup.find_all('h2'):
    a = h.find('a')
    cars.append(a.attrs['href'][10:])
    urls.append(a.attrs['href'])

import requests 
import pandas as pd
 
list_length = len(urls)
table = pd.DataFrame()

for x in range(list_length):
    page_link ='https://ev-database.uk' + urls[x]
             
    for i in range(0,10):
        next_table = pd.read_html(requests.get(page_link).content)[i]

        #if colum has * or † at the end, delete this symbols
        for row in range(len(next_table)):
            if next_table[0][row][-1] == '*':
                next_table[0][row] = next_table[0][row][0:-2]
            if next_table[0][row][-3] == '†':
                next_table[0][row] = next_table[0][row][0:-4]
        
        next_table[3] = cars[x]   
        table = table.append(next_table, ignore_index = True)
        print('in progress.... ' + cars[x])

#transform dataframe 
t2 = table.drop_duplicates(keep=False)
t3 = t2[~t2.index.duplicated(keep='first')]
t4 = t2.set_index([3,0])[1]
t5 = t4[~t4.index.duplicated(keep='first')]
t6 = t5.unstack()

#table_transformed = table.set_index([3,0])[1].unstack().rename_axis([None])

#select useful colums
table_selected = t6[['Battery Capacity', 'Charge Port', 'Charge Power', 
                                    'Charge Speed', 'Combined - Cold Weather', 'Combined - Mild Weather', 
                                    'Drive', 'Fastcharge Port', 'Fastcharge Power', 
                                    'Range', 'Top Speed', 'Total Power', 'Vehicle Consumption', 
                                    'Acceleration 0 - 62 mph', 
]]

# clean values in column "Charge Port" from nonetypes 
for i, r in table_selected.iterrows():
    if isinstance(r[1], float):
        r[1] = "-"
# clean values in column "Charge Power" from nonetypes
    if isinstance(r[2], float):
        r[2] = "-"
# clean values in column "Charge Speed" from nonetypes
    if isinstance(r[3], float):
        r[3] = "-"
# clean values in column "Drive" from nonetypes
    if isinstance(r[6], float):
        r[6] = "-"
# clean values in column "Fastcharge Power" from nonetypes
    if isinstance(r[8], float):
        r[8] = "-"
# clean values in column "Total Power" from nonetypes
    if isinstance(r[11], float):
        r[11] = "-"
# clean values in column "Vehicle Consumption" from nonetypes
    if isinstance(r[12], float):
        r[12] = "-"
# clean values in column "Battery Capacity" from "kWh" and convert values to float
    r[0] = float(r[0].replace(" kWh", ""))

# clean values in column "Combined - Cold Weather" from nonetypes (float) and convert values to float
for i, r in table_selected.iterrows():
    if isinstance(r[4], float):
        print("Wert: " + str(r[4]))
        r[4] = "0 mi"
for i, r in table_selected.iterrows():
    r[4] = round((float(r[4].replace("mi", ""))/0.621371), 2)
    
# clean values in column "Combined - Mild Weather" from nonetypes (float) and convert values to float
for i, r in table_selected.iterrows():
    if isinstance(r[5], float):
        print("Wert: " + str(r[5]))
        r[5] = "0 mi"
for i, r in table_selected.iterrows():
    r[5] = round((float(r[5].replace("mi", ""))/0.621371), 2)

# convert values in column "Range" to float
for i, r in table_selected.iterrows():
    r[9] = round((float(r[9].replace("mi", ""))/0.621371), 2)

# clean values in column "Top Speed" from nonetypes (float) and convert values to float
for i, r in table_selected.iterrows():
    if isinstance(r[10], float):
        print("Wert: " + str(r[10]))
        r[10] = "0 mph"
for i, r in table_selected.iterrows():
    r[10] = round((float(r[10].replace("mph", ""))/0.621371), 2)

# clean values in column "Acceleration 0 - 62 mph" from nonetypes (float) and convert values to float
for i, r in table_selected.iterrows():
    if isinstance(r[13], float):
        print("Wert: " + str(r[13]))
        r[13] = "0 sec"
for i, r in table_selected.iterrows():
    r[13] = float(r[13].replace("sec", ""))


import mysql.connector
connection = mysql.connector.connect(user='USER', password='PASSWORD',
                              host='mobility.f4.htw-berlin.de',
                              database='electric_vehicles')

# try / finally for potential erros in SQL queries

try:
   cursor = connection.cursor()
   for i, r in table_selected.iterrows():
       insertString = ("insert into electric_vehicles.vehicles (name, charge_port, "
                                              "charge_power, charge_speed, "
                                              "comb_cold_weather, comb_mild_weather, "
                                              "drive, fastcharge_port, fastcharge_power, "
                                              "range_km, top_speed, total_power, "
                                              "vehicle_consumption, acceleration, "
                                              "battery_capacity_kwh) values "
                                              "(%s, %s, %s, %s, %s, %s, %s, %s, %s, "
                                              "%s, %s, %s, %s, %s, %s)")
       data = (i, r[1], r[2], r[3], r[4], r[5],
               r[6], r[7], r[8], r[9], r[10], r[11], r[12], r[13], r[0])
       cursor.execute(insertString, data)
       print("Inserting car: " + str(i))
finally:
    connection.commit()
    connection.close()
