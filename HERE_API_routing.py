#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 14 23:08:19 2018

@author: jan-lukaspflaum
"""
import pandas as pd
import requests
import json

def geocoder(place):
    r = requests.get('https://geocoder.cit.api.here.com/6.2/geocode.json?app_id=jccZtyShstzovgbVxAJn&app_code=5ezWDCQaAJYiXldHFRV6gA&searchtext=' + place)
    place_geo = r.json()
    latitude = place_geo['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]['Latitude']
    longitude = place_geo['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]['Longitude']
    coordinates = str(latitude) + ',' + str(longitude)
    return coordinates

start = 'Alexanderplatz+Berlin'
destination = 'Schlossplatz+Stuttgart'

start_coord = geocoder(start)
destination_coord = geocoder(destination)

def here_route(start_coord, destination_coord):
    r = requests.get('https://route.cit.api.here.com/routing/7.2/calculateroute.json?app_id=jccZtyShstzovgbVxAJn&app_code=5ezWDCQaAJYiXldHFRV6gA&waypoint0='+ start_coord + '&waypoint1=' + destination_coord + '&mode=fastest;car;traffic:disabled')
    route = r.json()
    routeFrame = pd.DataFrame(route)  
    return routeFrame

routeFrame = here_route(start_coord,destination_coord)













days = []
prices = []

for i in range(len(routeFrame['dataset'][3])):
    day = routeFrame['dataset'][3][i][0]
    price = routeFrame['dataset'][3][i][2]
    days.append(day)
    prices.append(price)

df = pd.DataFrame(prices, days)

import matplotlib.pyplot as plt

plt.plot(days,prices)
plt.show()


view 
value? 
reuslt
value? 
location
NavigationPosition
value?
lat
LONG