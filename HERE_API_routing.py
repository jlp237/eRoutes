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
    return route

route = here_route(start_coord,destination_coord)

whole_trip_length_in_km = (route['response']['route'][0]['summary']['distance'])/1000
whole_trip_time_in_h = round((route['response']['route'][0]['summary']['baseTime'])/3600,3)


waypoints = []
lat_wp = []
lon_wp = []


for x in range(len(route['response']['route'][0]['leg'][0]['maneuver'])):
    wp = route['response']['route'][0]['leg'][0]['maneuver'][x]['length']
    lat = route['response']['route'][0]['leg'][0]['maneuver'][x]['position']['latitude']
    lon = route['response']['route'][0]['leg'][0]['maneuver'][x]['position']['longitude']
    waypoints.append(wp)
    lat_wp.append(lat)
    lon_wp.append(lon)


waypoints_with_coordinates = pd.DataFrame(
    {'waypoints': waypoints,
     'lat_wp': lat_wp,
     'lon_wp': lon_wp
    })

    

    
    

battery_level_at_start = 0.8
maximumRangeOfCar = 200
temparature = 20.0
security_puffer_in_km = 50 









distance_from_center = 'https://isoline.route.cit.api.here.com/routing/7.2/calculateisoline.json?mode=fastest;car;traffic:disabled&start=52.5160,13.3778&rangetype=distance&range=200000&app_id=jccZtyShstzovgbVxAJn&app_code=5ezWDCQaAJYiXldHFRV6gA'

import geopy.distance
coords_1 = (52.2296756, 21.0122287)
coords_2 = (52.406374, 16.9251681)
dist = geopy.distance.distance(coords_1, coords_2).km



