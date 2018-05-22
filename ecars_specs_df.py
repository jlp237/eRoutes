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
        print('in progress.... ' + cars[x])

#transform dataframe 
t2= table.drop_duplicates(keep=False)
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

#save as csv
table_selected.to_csv('eCars.csv', sep=';', encoding='utf-8')


#read csv

x = 'Porsche'
print(cars_frame[1:])

cars_frame = pd.read_csv('cars.csv',sep=';')
frame2 = cars_frame.set_index('Car', drop=True, append=False, inplace=False, verify_integrity=False)
car_data = (frame2.loc[x]['Range'])
car_range = car_data['Range']

#Select all cars in list
print(frame2['Range'])
print(cars_frame['Car'])

#Get list of all cars from csv
import pandas as pd
cars_frame = pd.read_csv('cars.csv',sep=';')
cars_list = cars_frame["Car"].tolist()
range_list = cars_frame["Range"].tolist()

#Get Range from Car X
import pandas as pd
x = 'Prosche'
cars_frame = pd.read_csv('cars.csv',sep=';')
frame2 = cars_frame.set_index('Car', drop=True, append=False, inplace=False, verify_integrity=False)
car_data = (frame2.loc[x]['Range'])

car_model = 'Bmw'
cars_frame = pd.read_csv("C:/Users/David/Desktop/cars.csv", sep=';')
frame2 = cars_frame.set_index('Car', drop=True, append=False, inplace=False, verify_integrity=False)
car_range = (frame2.loc[car_model]['Top Speed'])







