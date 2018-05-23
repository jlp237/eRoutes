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

# api call for getting the shape of route

def route_shape(start_coord, destination_coord):
    r = requests.get('https://route.api.here.com/routing/7.2/calculateroute.json?waypoint0='+ start_coord + '&waypoint1=' + destination_coord + '&mode=fastest;car;traffic:enabled&routeattributes=shape&app_id=jccZtyShstzovgbVxAJn&app_code=5ezWDCQaAJYiXldHFRV6gA')
    route = r.json()
    return route

route_shape = route_shape(start_coord,destination_coord)

# get lat/ lon of route shape 

lat_lon_1 = []

for x in range(len(route_shape['response']['route'][0]['shape'])):
    lat_lon = route_shape['response']['route'][0]['shape'][x]
    lat_lon_1.append(lat_lon)
 
    
# delete every second shape several times to reduce size  
# to do : write a loop that the list isnt too small (like only 10 elements, minimum elements = 160 ? )
    
del lat_lon_1[::2]
del lat_lon_1[::2]
del lat_lon_1[::2]
del lat_lon_1[::2]
del lat_lon_1[::2]

del lat_lon_1[0:40]

    
# convert to string
string_route_shapes = '|'.join(lat_lon_1)
string_route_shapes = '[' + string_route_shapes + ']'    

    
# parse shape to corridor api / is shape too big? / convert into polyline encoding of here maps
      
corridor_width = 1000
size_of_results = 100

def get_stations_along_route(string_route_shapes,corridor_width, size_of_results):
    r = requests.get('https://places.cit.api.here.com/places/v1/browse/by-corridor?app_id=jccZtyShstzovgbVxAJn&app_code=5ezWDCQaAJYiXldHFRV6gA&route=' +string_route_shapes + ';w=' + str(corridor_width)+ '&cat=ev-charging-station&size='+ str(size_of_results))
    stations = r.json()
    return stations


stations_along_route = get_stations_along_route(string_route_shapes,corridor_width, size_of_results)


# now calculate the nearest station of a radius of the range of the car (radius from the start-coordinates)


def coordinates_from_center(start, maximumRangeOfCar):
    r = requests.get('https://isoline.route.cit.api.here.com/routing/7.2/calculateisoline.json?mode=fastest;car;traffic:disabled&start='+ start +'&rangetype=distance&range=' + maximumRangeOfCar + '&app_id=jccZtyShstzovgbVxAJn&app_code=5ezWDCQaAJYiXldHFRV6gA')
    radius = r.json()
    return radius

maximumRangeOfCar = 200000
radius = coordinates_from_center(start_coord,str(maximumRangeOfCar))


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

min_dist = radius_coordinates_with_distances_from_center.loc[radius_coordinates_with_distances_from_center['distances_from_center'].idxmin()]
first_center_spot = min_dist['radius_coordinates']


# to do : compare first_center_spot with list of stations = nearest with geopy distance. 

stations_coordinates = []
for x in range(len(stations_along_route['results']['items'])):
    lat_1 = stations_along_route['results']['items'][x]['position'][0]
    lon_1 = stations_along_route['results']['items'][x]['position'][1]
    stations_coordinates.append(str(lat_1) + ',' + str(lon_1))
    
distances_station_from_first_center = []
for x in range(len(stations_coordinates)):
    coords_1 = stations_coordinates[x]
    coords_2 = first_center_spot
    dist = geopy.distance.distance(coords_1, coords_2).km
    distances_station_from_first_center.append(dist)

    
stations_coordinates_with_distances_from_center = pd.DataFrame(
    {
     'distances_station_from_first_center': distances_station_from_first_center,
     'stations_coordinates': stations_coordinates
    })

min_dist = stations_coordinates_with_distances_from_center.loc[stations_coordinates_with_distances_from_center['distances_station_from_first_center'].idxmin()]
first_station = min_dist['stations_coordinates']

# input = min dist = coord and line number of first station , now get data from station. 

# neuer ansatz: schleife bauen , die eine route berechnet bis zum ersten polyline punkt, checkt ob gefahrene distanz < range of car ist. 
#  gefahrene distanz darf nicht > range sein. dann nimmt die funktion sich die koordinate von wegpunkt 200 km. 
# loop durchläuft alle abstände zwischen koordinate und stationen along route. es wird station zurückgegeben mit kleinstem abstand zur station. 
#wenn größer als range , dann in stationsliste eintrag x-1 (= eine station davor) auswählen == erste ladestation


# berechne route 

def route_to_polyline_point(start_coord, destination_coord):
    r = requests.get('https://route.cit.api.here.com/routing/7.2/calculateroute.json?app_id=jccZtyShstzovgbVxAJn&app_code=5ezWDCQaAJYiXldHFRV6gA&waypoint0='+ start_coord + '&waypoint1=' + destination_coord + '&mode=fastest;car;traffic:disabled')
    route = r.json()
    return route


# how long in m is the route ? 


# while loop: 

distance_polypoint_to_start = 0
x = 0
route_to_polyline_point_length_in_m = 0
while distance_polypoint_to_start <= 200000:
    #take polyline punkt 
    route = route_to_polyline_point(start_coord,str(lat_lon_1[x]))
    route_to_polyline_point_length_in_m = (route['response']['route'][0]['summary']['distance'])
    distance_polypoint_to_start = route_to_polyline_point_length_in_m
    x += 1
    
lat_lon_1[x]

# data from first station


station_openingHours = stations_along_route['results']['items'][x]['openingHours']['text']
station_position = str(stations_along_route['results']['items'][x]['position'][0])+ ','+ str(stations_along_route['results']['items'][x]['position'][1])
station_title = stations_along_route['results']['items'][x]['title']




# to do:   check if distance from 1. station to destination is greater than range of car ! 
# if yes , search next station after the first station! 
# loop ! 



# for visualization: 
# https://developer.here.com/api-explorer/geovisualization/technology_markers/markers-csv-provider

# to do: 

#build some loops
#integrate security puffer 
#integrate in temperature
#integrate battery level at start

temparature = 20.0
battery_level_at_start = 0.8
security_puffer_in_km = 50 


# to do : 

#put all input values to top !


