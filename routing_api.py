# -*- coding: utf-8 -*-
"""
Created on Tue May 22 13:43:29 2018

@author: David
"""

#Routing API
#https://maps.googleapis.com/maps/api/directions/json?origin=New+York,+NY&destination=Boston,+MA&waypoints=optimize:true|Providence,+RI|Hartford,+CT&key='

import requests
import pandas as pd


def get_direction_data(start, destination):

    api_key = 'AIzaSyAonN5q0C_6Vlvm8VGIWPd-vl43vjJqca0'
    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'  
    waypoint_array = ["Frankfurt", "München", "Paris"]

    #create waypoints strings
    waypoint_counter = 1
    waypoint_map_string = ""
    waypoint_request_string = ""
    for waypoint in waypoint_array:
        waypoint_map_string += 'location' + str(waypoint_counter) + '=' + waypoint + '&'
        waypoint_request_string += waypoint + '|' 
        waypoint_counter += 1
    waypoints_return = waypoint_map_string[:-1]
    waypoints = waypoint_request_string[:-1]

    #make request for routing json  
    nav_request = 'origin={}&destination={}&waypoints={}&key={}'.format(start, destination, waypoints, api_key)
    url = endpoint + nav_request
    json_data = requests.get(url).json()
    routes = json_data['routes']

    #prepare return json
    data = {
        'routes': routes,
        'waypoints_return': waypoints_return,
    }
    return data




route = get_direction_data("Berlin", "Madrid")





charging_stations_array = []
for i in range(len(route['routes'][0]['legs'])):
    charging_station = route['routes'][0]['legs']

    charging_stations_array.append(charging_station)


stations = route['routes'][0]['legs'][i]['distance']['text']

time = route['routes'][0]['legs'][0]['duration']['value']

charging_stations_array = []
for i in range(len(charging_station)):
    address = charging_station[i]['end_address']
    distance = charging_station[i]['distance']['text']
    duration = charging_station[i]['duration']['text']
    text = address + ';' + distance + ';' + duration 
    charging_stations_array.append(text)


range = "100 km"
range = range[:-2]
range_num = int(int(range) * 1.6)

x = (str(charging_station))
x[1]['end_address']

for waypoint in charging_station:
    print(waypoint['end_address'])


#Total Distance
distance_array = []
for i in range(len(route['routes'][0]['legs'])):
    charging_station = route['routes'][0]['legs'][i]['distance']['value']
    distance_array.append(charging_station)

total_distance = sum(distance_array)

#Driving Time
driving_time_array = []
for i in range(len(route['routes'][0]['legs'])):
    charging_station = route['routes'][0]['legs'][i]['duration']['value']
    driving_time_array.append(charging_station)

driving_time = sum(driving_time_array)

