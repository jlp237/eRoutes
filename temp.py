#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 23 10:54:30 2018

@author: jan-lukaspflaum
"""



waypoints_0 = []
lat_wp = []
lon_wp = []


for x in range(len(route['response']['route'][0]['leg'][0]['maneuver'])):
    wp = route['response']['route'][0]['leg'][0]['maneuver'][x]['length']
    lat = route['response']['route'][0]['leg'][0]['maneuver'][x]['position']['latitude']
    lon = route['response']['route'][0]['leg'][0]['maneuver'][x]['position']['longitude']
    waypoints_0.append(wp)
    lat_wp.append(lat)
    lon_wp.append(lon)
#
#
waypoints_with_coordinates = pd.DataFrame(
    {
     'lat_wp': lat_wp,
     'lon_wp': lon_wp
    })
   
    
    ######################
    
    
    def stations_near_center(coord):
    r = requests.get('https://places.cit.api.here.com/places/v1/browse?at='+ coord +'&cat=ev-charging-station&app_id=jccZtyShstzovgbVxAJn&app_code=5ezWDCQaAJYiXldHFRV6gA')
    stations = r.json()
    return stations

######################
    

i = 0 
dist = 0 

while dist <= maximumRangeOfCar - waypoints_with_coordinates['waypoints'][i+1]:
    dist = dist + waypoints_with_coordinates['waypoints'][i]
    i += 1
    
first_stop_lat = waypoints_with_coordinates['lat_wp'][i]
first_stop_lon = waypoints_with_coordinates['lon_wp'][i]





