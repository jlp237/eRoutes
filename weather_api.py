# -*- coding: utf-8 -*-
"""
Created on Sun May  6 11:57:10 2018

@author: David
"""

#Waether API
import requests
api_address='http://api.openweathermap.org/data/2.5/weather?appid=31d7b827392ab249e871954306d44d04&q='
#city = input('City Name :')
city = 'Berlin'
url = api_address + city
json_data = requests.get(url).json()
kelvin = json_data['main']['temp']
temperature = round(kelvin - 273.15,0)
print(temperature)


#Geo_Location API
api_key = 'AIzaSyCSLetZcqVMjiQMdfR7mudMe5bwzWIYzqo'
location = 'Burgrieden'
url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+location+'&key='+api_key
json_data = requests.get(url).json()
geo_data = json_data['results'][0]['geometry']['location']



lat = round(geo['lat'],1)
lng = round(geo['lng'],1)

geo_data = {
    'lat': lat,
    'lng': lng,
}



