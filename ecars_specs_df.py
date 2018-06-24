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
            if next_table[0][row][-4:-1] == ' † *':
                next_table[0][row] = next_table[0][row][0:-4]
            if next_table[0][row][-1] == '†':
                next_table[0][row] = next_table[0][row][0:-2]
            if next_table[0][row][-1] == '*':
                next_table[0][row] = next_table[0][row][0:-2]
            if next_table[0][row][:11] == 'Charge Time':
                next_table[0][row] = next_table[0][row][0:12]
            if next_table[0][row][:15] == 'Fastcharge Time':
                next_table[0][row] = next_table[0][row][0:16]
           

        
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
                                    'Acceleration 0 - 62 mph', 'Charge Time ', 'Fastcharge Time ',
                                    'Battery Useabl'
]]

# clean values in column "Charge Port" from nonetypes 
for i, r in table_selected.iterrows():
    if not isinstance(r[1], str):
        r[1] = "-"
# clean values in column "Charge Power" from nonetypes
    if not isinstance(r[2], str):
        r[2] = "-"
# clean values in column "Charge Speed" from nonetypes
    if not isinstance(r[3], str):
        r[3] = "-"
# clean values in column "Combined - Cold Weather" from nonetypes
    if not isinstance(r[4], str):
        r[4] = "-"
# clean values in column "Combined - Mild Weather" from nonetypes
    if not isinstance(r[5], str):
        r[5] = "-"
# clean values in column "Drive" from nonetypes
    if not isinstance(r[6], str):
        r[6] = "-"
# clean values in column "Fastcharge Power" from nonetypes
    if not isinstance(r[8], str):
        r[8] = "-"
# clean values in column "Top Speed" from nonetypes
    if not isinstance(r[10], str):
        r[10] = "-"
# clean values in column "Total Power" from nonetypes
    if not isinstance(r[11], str):
        r[11] = "-"
# clean values in column "Acceleration 0 - 62 mph" from nonetypes
    if not isinstance(r[13], str):
        r[13] = "-"
# clean values in column "Fastcharge Time" from nonetypes
    if not isinstance(r[15], str):
        r[15] = "-"
# clean values in column "Battery Usabl" from nonetypes
    if not isinstance(r[16], str):
        r[16] = "-"
# clean values in column "Battery Capacity" from "kWh" and convert values to float
    r[0] = float(r[0].replace(" kWh", ""))


for i, r in table_selected.iterrows():
    # clean values in column "Combined - Cold Weather" from nonetypes (float) and convert values to float
    if r[4] == '-':
        r[4] = "0 mi"
    r[4] = round((float(r[4].replace("mi", ""))/0.621371), 2) 
    # clean values in column "Combined - Mild Weather" from nonetypes (float) and convert values to float
    if r[5] == '-':
        r[5] = "0 mi"
    r[5] = round((float(r[5].replace("mi", ""))/0.621371), 2)
    # convert values in column "Range" to float
    r[9] = round((float(r[9].replace("mi", ""))/0.621371), 2)
    # clean values in column "Top Speed" from nonetypes (float) and convert values to float
    if r[10] == '-':
        r[10] = "0 mph"
    r[10] = round((float(r[10].replace("mph", ""))/0.621371), 2)
    # clean values in column "Acceleration 0 - 62 mph" from nonetypes (float) and convert values to float
    if r[13] == '-':
        r[13] = "0 sec"
    r[13] = float(r[13].replace("sec", ""))
