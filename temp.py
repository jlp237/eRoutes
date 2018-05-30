#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 23 10:54:30 2018

@author: jan-lukaspflaum
"""

# neuer ansatz: schleife bauen , die eine route berechnet bis zum ersten polyline punkt, checkt ob gefahrene distanz < range of car ist. 
#  gefahrene distanz darf nicht > range sein. dann nimmt die funktion sich die koordinate von wegpunkt 200 km. 
# loop durchläuft alle abstände zwischen koordinate und stationen along route. es wird station zurückgegeben mit kleinstem abstand zur station. 
#wenn größer als range , dann in stationsliste eintrag x-1 (= eine station davor) auswählen == erste ladestation


# for visualization: 
# https://developer.here.com/api-explorer/geovisualization/technology_markers/markers-csv-provider

# to do: 

#integrate security puffer 

#integrate in temperature
#integrate battery level at start

temparature = 20.0
battery_level_at_start = 0.8
security_puffer_in_km = 50 



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 14 23:08:19 2018

@author: jan-lukaspflaum
"""
import pandas as pd
import requests
import geopy.distance

# 1. all neccessary functions are listed here: 

# a geocoder that translates an address or given place from a string into coordinates

def geocoder(place):
    r = requests.get('https://geocoder.cit.api.here.com/6.2/geocode.json?app_id=jccZtyShstzovgbVxAJn&app_code=5ezWDCQaAJYiXldHFRV6gA&searchtext=' + place)
    place_geo = r.json()
    latitude = place_geo['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]['Latitude']
    longitude = place_geo['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]['Longitude']
    coordinates = str(latitude) + ',' + str(longitude)
    return coordinates

# an api request that returns a route between two given waypoints

def here_route(start_coord, destination_coord):
    r = requests.get('https://route.cit.api.here.com/routing/7.2/calculateroute.json?app_id=jccZtyShstzovgbVxAJn&app_code=5ezWDCQaAJYiXldHFRV6gA&waypoint0='+ start_coord + '&waypoint1=' + destination_coord + '&mode=fastest;car;traffic:disabled')
    route = r.json()
    return route

# an api request that returns the shape of a route between two given waypoints as an object with many many coordinates 

def route_shape(start_coord, destination_coord):
    r = requests.get('https://route.api.here.com/routing/7.2/calculateroute.json?waypoint0='+ start_coord + '&waypoint1=' + destination_coord + '&mode=fastest;car;traffic:enabled&routeattributes=shape&app_id=jccZtyShstzovgbVxAJn&app_code=5ezWDCQaAJYiXldHFRV6gA')
    route = r.json()
    return route

# an api request that returns all stations along a route in specified corridor around the route

def get_stations_along_route(string_route_shapes,corridor_width, size_of_results):
    r = requests.get('https://places.cit.api.here.com/places/v1/browse/by-corridor?app_id=jccZtyShstzovgbVxAJn&app_code=5ezWDCQaAJYiXldHFRV6gA&route=' +string_route_shapes + ';w=' + str(corridor_width)+ '&cat=ev-charging-station&size='+ str(size_of_results))
    stations = r.json()
    return stations

def complete_route(fe_start, fe_dest, range_of_car):
    # api call for geocoding strings into coordinates
    start_coord = geocoder(start)
    destination_coord = geocoder(destination)
    list_of_waypoints = []
    list_of_waypoints.append(start_coord)
    # api call for route calculation
    print("1")
    route = here_route(start_coord,destination_coord)
    trip_length_in_m = (route['response']['route'][0]['summary']['distance'])
    if trip_length_in_m > range_of_car:
        # api call for getting the shape of route
        route_poly_shape = route_shape(start_coord,destination_coord)
        # get lat/ lon of route shape 
        polyline_coordinates = []
        for x in range(len(route_poly_shape['response']['route'][0]['shape'])):
            lat_lon = route_poly_shape['response']['route'][0]['shape'][x]
            polyline_coordinates.append(lat_lon)
        # delete every second shape several times to reduce size until size > 160
        print("2")
        while len(polyline_coordinates) > 160:
            del polyline_coordinates[::2]
        # convert Polyline to string for api call
        string_route_shape = '|'.join(polyline_coordinates)
        string_route_shape = '[' + string_route_shape + ']'
        # set corridor width and result size then parse shape to corridor api and get the stations along the route
        corridor_width = 2000
        size_of_results = 200
        stations_along_route = get_stations_along_route(string_route_shape,corridor_width, size_of_results)
        #create list with all coordinates of the found stations
        stations_coordinates = []
        for x in range(len(stations_along_route['results']['items'])):
            lat_1 = stations_along_route['results']['items'][x]['position'][0]
            lon_1 = stations_along_route['results']['items'][x]['position'][1]
            stations_coordinates.append(str(lat_1) + ',' + str(lon_1))
        # calculating how many stations needed to be found during the trip. 
        print("3")
        loops = int((trip_length_in_m/range_of_car))
        #select the first guess for a polyline point by dividing the list of polyline points by the rounded number of loops
        first_polyline_point = int((len(polyline_coordinates))/loops)
        #loop for all stations during trip
        a = 1
        print("4")
        while a <= (loops):
            distance_polypoint_to_start = 0
            # loop to find polypoint on route after range of car
            # calculate route between start and polyline point
            print(first_polyline_point)
            route = here_route(start_coord,polyline_coordinates[first_polyline_point])
            # get distance
            route_to_polyline_point_length_in_m = (route['response']['route'][0]['summary']['distance'])
            # raise counter by distance of route
            distance_polypoint_to_start = route_to_polyline_point_length_in_m
            print(distance_polypoint_to_start)

            
            if distance_polypoint_to_start >= range_of_car:
                first_polyline_point = int(first_polyline_point/2)
                distance_polypoint_to_start = 0
                print(distance_polypoint_to_start)

                print("if")
                print(first_polyline_point)
            else:
                # raise counter for next polyline point
                first_polyline_point += 2
                print("else")
                print(first_polyline_point)
            while distance_polypoint_to_start <= range_of_car and first_polyline_point <= int(len(polyline_coordinates)):
                route = here_route(start_coord,polyline_coordinates[first_polyline_point])
                # get distance
                route_to_polyline_point_length_in_m = (route['response']['route'][0]['summary']['distance'])
                # raise counter by distance of route
                distance_polypoint_to_start = route_to_polyline_point_length_in_m
                first_polyline_point += 2
                print("while")
                print(first_polyline_point)
                print(distance_polypoint_to_start)
            #get the calculated polyline point
            first_found_polypoint = polyline_coordinates[first_polyline_point]
            # calculate distances from polyline point to all stations along route, take the nearest station
            print("5")
            distances_station_from_found_polypoint = []
            for z in range(len(stations_coordinates)):
                coords_1 = stations_coordinates[z]
                coords_2 = first_found_polypoint
                dist = geopy.distance.distance(coords_1, coords_2).km
                distances_station_from_found_polypoint.append(dist)
            stations_coordinates_with_distances_station_from_found_polypoint = pd.DataFrame({'distances_station_from_found_polypoint': distances_station_from_found_polypoint,'stations_coordinates': stations_coordinates})
            row_of_station = stations_coordinates_with_distances_station_from_found_polypoint['distances_station_from_found_polypoint'].idxmin()
            
            print("6")
            # get data from station
            #station_openingHours = stations_along_route['results']['items'][row_of_station]['openingHours']['text']
            station_position = str(stations_along_route['results']['items'][row_of_station]['position'][0])+ ','+ str(stations_along_route['results']['items'][row_of_station]['position'][1])
            #station_title = stations_along_route['results']['items'][row_of_station]['title']
            list_of_waypoints.append(station_position)
            start_coord = station_position
            print(first_polyline_point)
            print(a)
            first_polyline_point = int((int((len(polyline_coordinates))/loops))*1.5)
            stations_coordinates_with_distances_station_from_found_polypoint = []
            row_of_station = 0
            a += 1
    else: 
        print("no need to carge during this trip. The Battery of the car will last")
    list_of_waypoints.append(destination_coord)
    return list_of_waypoints
    
#################################################################################
# TEST SECTION
#################################################################################

start = 'Berlin ,Weserstrasse 12'
destination = 'Schlossplatz+Stuttgart'
range_of_car = 200000
list_of_waypoints = complete_route(start, destination, range_of_car)
