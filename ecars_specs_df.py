# -*- coding: utf-8 -*-
"""
Created on Sun May  6 12:37:15 2018

@author: Jan-Lukas, David
"""

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
        print('in progress.... ' + x + '/63' + cars[x])

#transform dataframe 
table_transformed = table.set_index([3,0])[1].unstack().rename_axis([None])

#select useful colums
table_selected = table_transformed[['Battery Capacity', 'Charge Port', 'Charge Power', 
                                    'Charge Speed', 'Combined - Cold Weather', 'Combined - Mild Weather', 
                                    'Drive', 'Electric Range', 'Fastcharge Port', 'Fastcharge Power', 
                                    'Range', 'Top Speed', 'Total Power', 'Vehicle Consumption', ]]

#save as csv
table_selected.to_csv('cars4.csv', sep=';', encoding='utf-8')


#read csv
cars_frame = pd.read_csv('cars4.csv',sep=';')
print(cars_frame[1][3])

