# -*- coding: utf-8 -*-
"""
Created on Thu May 24 23:17:17 2018

@author: David
"""

#Geo_Location API
import requests
api_key = 'AIzaSyCSLetZcqVMjiQMdfR7mudMe5bwzWIYzqo'
location = 'Germany'
url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+location+'&key='+api_key
json_data = requests.get(url).json()
geo = json_data['results'][0]['geometry']['location']



lat = round(geo['lat'],1)
lng = round(geo['lng'],1)

geo_data = {
    'lat': lat,
    'lng': lng,
}