#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 14 23:08:19 2018

@author: jan-lukaspflaum
"""
import pandas as pd
import requests
import geopy.distance
import time
start_time = time.time()



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
    route = here_route(start_coord,destination_coord)
    trip_length_in_m = (route['response']['route'][0]['summary']['distance'])
    print('1')
    if trip_length_in_m > range_of_car:
        # api call for getting the shape of route
        route_poly_shape = route_shape(start_coord,destination_coord)
        # get lat/ lon of route shape 
        polyline_coordinates = []
        for x in range(len(route_poly_shape['response']['route'][0]['shape'])):
            lat_lon = route_poly_shape['response']['route'][0]['shape'][x]
            polyline_coordinates.append(lat_lon)
        # calculating how many stations needed to be found during the trip.
        loops = round((trip_length_in_m/range_of_car))
        # delete every second shape several times to reduce size until size > 4700 characters
        delete_range = int((len(polyline_coordinates))/(loops+5))
        del polyline_coordinates[0:delete_range]
        if trip_length_in_m < 600000:
            while len(polyline_coordinates) > 160:
                print('while1')
                del polyline_coordinates[::2]
        else:
            while len(polyline_coordinates) > 220:
                print('while2')
                del polyline_coordinates[::2]
        print('2')
        
        # convert Polyline to string for api call
        string_route_shape = '|'.join(polyline_coordinates)
        string_route_shape = '[' + string_route_shape + ']'
        # set corridor width and result size then parse shape to corridor api and get the stations along the route
        corridor_width = 3000
        size_of_results = 300
        stations_along_route = get_stations_along_route(string_route_shape,corridor_width, size_of_results)
        #create list with all coordinates of the found stations
        stations_coordinates = []
        for x in range(len(stations_along_route['results']['items'])):
            lat_1 = stations_along_route['results']['items'][x]['position'][0]
            lon_1 = stations_along_route['results']['items'][x]['position'][1]
            stations_coordinates.append(str(lat_1) + ',' + str(lon_1))        
            
        #loop for all stations during trip
        first_polyline_point = 0
        a = 1
        while a <= loops:
            print('while3')
            if a == 1:
                print('if 1')
                # select the geocoordinates from a point on the route that equals the range of the car
                found = False           
                while found == False:
                    print('while4')
                    #route to first point in list:
                    route = here_route(start_coord,polyline_coordinates[first_polyline_point])
                    # get distance
                    route_to_polyline_point_length_in_m = (route['response']['route'][0]['summary']['distance'])
                    if route_to_polyline_point_length_in_m < range_of_car:
                        first_polyline_point += 2
                        print('if 2')
                    else:
                        print('else1')
                        found = True
                        first_polyline_point -= 2
            else:
                print('else2')
                route = here_route(start_coord,polyline_coordinates[first_polyline_point])
                route_to_polyline_point_length_in_m = (route['response']['route'][0]['summary']['distance'])
                while route_to_polyline_point_length_in_m > range_of_car: 
                    print('while5')
                    first_polyline_point -= 2
                    route = here_route(start_coord,polyline_coordinates[first_polyline_point])
                    route_to_polyline_point_length_in_m = (route['response']['route'][0]['summary']['distance'])
                    
                if route_to_polyline_point_length_in_m < range_of_car:
                    print('if 3')
                    while route_to_polyline_point_length_in_m < range_of_car:
                        print('while6')
                        first_polyline_point += 2
                        route = here_route(start_coord,polyline_coordinates[first_polyline_point])
                        route_to_polyline_point_length_in_m = (route['response']['route'][0]['summary']['distance'])
                if route_to_polyline_point_length_in_m > range_of_car:
                    print('if 4')
                    first_polyline_point -= 2
                    
                    
            #get the calculated polyline point
            first_found_polypoint = polyline_coordinates[first_polyline_point]
            # calculate distances from polyline point to all stations along route, take the nearest station
            distances_station_from_found_polypoint = []
            for z in range(len(stations_coordinates)):
                coords_1 = stations_coordinates[z]
                coords_2 = first_found_polypoint
                dist = geopy.distance.distance(coords_1, coords_2).km
                distances_station_from_found_polypoint.append(dist)
            stations_coordinates_with_distances_station_from_found_polypoint = pd.DataFrame({'distances_station_from_found_polypoint': distances_station_from_found_polypoint,'stations_coordinates': stations_coordinates})
            row_of_station = stations_coordinates_with_distances_station_from_found_polypoint['distances_station_from_found_polypoint'].idxmin()
            
            # get data from station
            #station_openingHours = stations_along_route['results']['items'][row_of_station]['openingHours']['text']
            #station_title = stations_along_route['results']['items'][row_of_station]['title']
            station_position = str(stations_along_route['results']['items'][row_of_station]['position'][0])+ ','+ str(stations_along_route['results']['items'][row_of_station]['position'][1])
            route = here_route(start_coord,station_position)
            dist_to_station = (route['response']['route'][0]['summary']['distance'])
            
            while dist_to_station > range_of_car:
                print('while7')
                row_of_station -= 1
                print(row_of_station)
                station_position = str(stations_along_route['results']['items'][row_of_station]['position'][0])+ ','+ str(stations_along_route['results']['items'][row_of_station]['position'][1])
                print(station_position)
                route = here_route(start_coord,station_position)
                dist_to_station = (route['response']['route'][0]['summary']['distance'])
                print(dist_to_station)
                
            list_of_waypoints.append(station_position)
            start_coord = station_position
            if a == 1:
                print('if 5')
                first_polyline_point = int((len(polyline_coordinates)/loops))
            else:
                print('else 3')
                first_polyline_point += int((len(polyline_coordinates)/loops)) 
                
            stations_coordinates_with_distances_station_from_found_polypoint = []
            row_of_station = 0
            a += 1
    else: 
        print("no need to carge during this trip. The Battery of the car will last")
    list_of_waypoints.append(destination_coord)
    print("--- %s seconds ---" % (time.time() - start_time))
    return list_of_waypoints
    
#################################################################################
# TEST SECTION
##########################a#######################################################

start = 'Berlin'
destination = 'Paris'
range_of_car = 200000
list_of_waypoints = complete_route(start, destination, range_of_car)

url = ''
for x in range(len(list_of_waypoints)):
    url += str(list_of_waypoints[x]) + '/'
google = 'https://www.google.com/maps/dir/' + url
print(google)
