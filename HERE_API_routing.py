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

min_dist = radius_coordinates_with_distances_from_center.loc[radius_coordinates_with_distances_from_center['distances_from_center'].idxmin()]
first_center_spot = min_dist['radius_coordinates']



# to do : umkreissuche um den radius nach EV charging station / poi / category = ev station 


def stations_near_center(coord):
    r = requests.get('https://places.cit.api.here.com/places/v1/browse?at='+ coord +'&cat=ev-charging-station&app_id=jccZtyShstzovgbVxAJn&app_code=5ezWDCQaAJYiXldHFRV6gA')
    stations = r.json()
    return stations


stations_result = stations_near_center(first_center_spot)


station_distance_to_center = stations_result['results']['items'][0]['distance']
station_openingHours = stations_result['results']['items'][0]['openingHours']
station_position = stations_result['results']['items'][0]['position']
station_title = stations_result['results']['items'][0]['title']


# testen ob routenanweisungen für korridor geeignet sind 
# convert waypoint list to string with trennzeichen |

waypoints_with_coordinates.to_string(header=False, index=False)

waypoints_string= ''

for x in range(len(waypoints_with_coordinates)):
    var1 = waypoints_with_coordinates['lat_wp'][x]
    var2 = waypoints_with_coordinates['lon_wp'][x]
    waypoints_string = waypoints_string + str(var1) + ',' + str(var2) + '|'
    
# to do : delete last '|' 



waypoints = '[52.7074,13.1926|52.7045,13.0661|52.7191,12.9621|52.7636,12.8263|52.7861,12.8000|52.8335,12.7919|52.9002,12.7451|52.9708,12.6311|53.0526,12.5392|53.0867,12.5169|53.1146,12.4687|53.1334,12.4644|53.1415,12.4225|53.1666,12.3722|53.1785,12.3050|53.2570,12.1618|53.2893,12.0618|53.3000,11.9373|53.3316,11.8724|53.3463,11.8190|53.3669,11.7328|53.3725,11.6427|53.4154,11.5505|53.4309,11.4906|53.4342,11.4000|53.4655,11.3370|53.4873,11.2631|53.4860,11.2011|53.5110,10.9647|53.5128,10.8414|53.5495,10.6892|53.5692,10.5155|53.5596,10.4259|53.5682,10.2999|53.5571,10.2020|53.5672,10.1279|53.5534,9.9924]'
corridor_width = 4000
size_of_results = 100

def get_stations_along_route(waypoints,corridor_width, size_of_results):
    r = requests.get('http://places.cit.api.here.com/places/v1/browse?route='+ waypoints +';w='+ str(corridor_width) +'&cat=ev-charging-station&size='+ str(size_of_results) +'&Accept-Language=de-de&app_id=jccZtyShstzovgbVxAJn&app_code=5ezWDCQaAJYiXldHFRV6gA')
    stations = r.json()
    return stations


stations_along_route = get_stations_along_route(waypoints,corridor_width, size_of_results)


#korridor sehr klein und schauen , welche gefundene station nahe des startpunktes ist (radius suche )







# browse by corridor : 
#https://places.cit.api.here.com/places/v1/browse/by-corridor?app_id=jccZtyShstzovgbVxAJn&app_code=5ezWDCQaAJYiXldHFRV6gA&route=[52.5160,13.3771|52.5111,13.3712|52.5355,13.3634|52.5400,13.3704|52.5626,13.3307|52.5665,13.3076|52.6007,13.2806|52.6135,13.2484|52.6303,13.2406|52.6651,13.2410|52.7074,13.1926|52.7045,13.0661|52.7191,12.9621|52.7636,12.8263|52.7861,12.8000|52.8335,12.7919|52.9002,12.7451|52.9708,12.6311|53.0526,12.5392|53.0867,12.5169|53.1146,12.4687|53.1334,12.4644|53.1415,12.4225|53.1666,12.3722|53.1785,12.3050|53.2570,12.1618|53.2893,12.0618|53.3000,11.9373|53.3316,11.8724|53.3463,11.8190|53.3669,11.7328|53.3725,11.6427|53.4154,11.5505|53.4309,11.4906|53.4342,11.4000|53.4655,11.3370|53.4873,11.2631|53.4860,11.2011|53.5110,10.9647|53.5128,10.8414|53.5495,10.6892|53.5692,10.5155|53.5596,10.4259|53.5682,10.2999|53.5571,10.2020|53.5672,10.1279|53.5534,9.9924];w=1000&cat=ev-charging-station&pretty
# por just browse? https://developer.here.com/documentation/places/topics_api/resource-browse.html


# for visualization: 
# https://developer.here.com/api-explorer/geovisualization/technology_markers/markers-csv-provider


