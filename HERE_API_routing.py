#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 14 23:08:19 2018

@author: jan-lukaspflaum
"""
import pandas as pd
import requests

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


#
#waypoints = []
#lat_wp = []
#lon_wp = []
#
#
#for x in range(len(route['response']['route'][0]['leg'][0]['maneuver'])):
#    wp = route['response']['route'][0]['leg'][0]['maneuver'][x]['length']
#    lat = route['response']['route'][0]['leg'][0]['maneuver'][x]['position']['latitude']
#    lon = route['response']['route'][0]['leg'][0]['maneuver'][x]['position']['longitude']
#    waypoints.append(wp)
#    lat_wp.append(lat)
#    lon_wp.append(lon)
#
#
#waypoints_with_coordinates = pd.DataFrame(
#    {'waypoints': waypoints,
#     'lat_wp': lat_wp,
#     'lon_wp': lon_wp
#    })
    
battery_level_at_start = 0.8
maximumRangeOfCar = 200000
temparature = 20.0
security_puffer_in_km = 50 

#
#i = 0 
#dist = 0 
#
#while dist <= maximumRangeOfCar - waypoints_with_coordinates['waypoints'][i+1]:
#    dist = dist + waypoints_with_coordinates['waypoints'][i]
#    i += 1
#    
#first_stop_lat = waypoints_with_coordinates['lat_wp'][i]
#first_stop_lon = waypoints_with_coordinates['lon_wp'][i]




def coordinates_from_center(start, range_from_center):
    r = requests.get('https://isoline.route.cit.api.here.com/routing/7.2/calculateisoline.json?mode=fastest;car;traffic:disabled&start='+ start +'&rangetype=distance&range=' + range_from_center + '&app_id=jccZtyShstzovgbVxAJn&app_code=5ezWDCQaAJYiXldHFRV6gA')
    radius = r.json()
    return radius

range_in_m = 200000

#start_coord = geocoder(start)

radius = coordinates_from_center(start_coord,str(range_in_m))
radius_coordinates = []
for x in range(len(radius['response']['isoline'][0]['component'][0]['shape'])):
    radius_coordinate = radius['response']['isoline'][0]['component'][0]['shape'][x]
    radius_coordinates.append(radius_coordinate)
    
import geopy.distance
distances_from_center = []
for x in range(len(radius_coordinates)):
    coords_1 = radius_coordinates[x]
    coords_2 = destination_coord
    dist = geopy.distance.distance(coords_1, coords_2).km
    distances_from_center.append(dist)

    
    
    
radius_coordinates_with_distances_from_center = pd.DataFrame(
    {
     'distances_from_center': distances_from_center,
     'radius_coordinates': radius_coordinates
    })

import geopy.distance
coords_1 = (52.2296756, 21.0122287)
coords_2 = (52.406374, 16.9251681)
dist = geopy.distance.distance(coords_1, coords_2).km



# to do : umkreissuche um den radius nach EV charging station / poi / category = ev station 
