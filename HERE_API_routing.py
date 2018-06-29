#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 10:23:00 2018

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


# an api request that returns a route between two given waypointsa
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


def trip_length(start_coord,destination_coord):
    route = here_route(start_coord,destination_coord)
    trip_length_in_m = (route['response']['route'][0]['summary']['distance'])
    return trip_length_in_m


def get_station_list(poly_start,polyline_coordinates,stations_coordinates,corridor_width, size_of_results, reverse):
    if reverse == True: 
        route_poly_shape = route_shape(polyline_coordinates,poly_start)
    if reverse == False:
        route_poly_shape = route_shape(poly_start, polyline_coordinates)
    segment_polyline_coordinates = route_poly_shape['response']['route'][0]['shape']
    while len(segment_polyline_coordinates) > 160:
        print('segment poly coord löschen')
        del segment_polyline_coordinates[::2]
    segment_string_route_shape = '|'.join(segment_polyline_coordinates)
    segment_string_route_shape = '[' + segment_string_route_shape + ']'
    stations_along_route = get_stations_along_route(segment_string_route_shape,corridor_width, size_of_results)
    temp_stations = []
    for x in range(len(stations_along_route['results']['items'])):
        lat_1 = stations_along_route['results']['items'][x]['position'][0]
        lon_1 = stations_along_route['results']['items'][x]['position'][1]
        temp_stations.append(str(lat_1) + ',' + str(lon_1))
    if reverse == True: 
        temp_stations.reverse()
    stations_coordinates.extend(temp_stations)
    stations_coordinates = list(dict.fromkeys(stations_coordinates))
    print("neue stationsliste stationsanzahl = " + str(len(stations_coordinates)))
    return stations_coordinates


def complete_route(start, destination, range_of_car, percentage_range_at_start):#, battery_status):
    # set corridor width and result size then parse shape to corridor api and get the stations along the route
    start_range = int(range_of_car*percentage_range_at_start)
    real_range = range_of_car
    #range_of_car = int(range_of_car*0.96)
    corridor_width = 3000
    size_of_results = 300
    old_polyline_point = 0
    # api call for geocoding strings into coordinates
    start_coord = geocoder(start)
    destination_coord = geocoder(destination)
    list_of_waypoints = []
    list_of_waypoints.append(start_coord)
    # api call for route calculation
    trip_length_in_m = trip_length(start_coord, destination_coord)
    print('1')
    if trip_length_in_m > range_of_car:
        # api call for getting the shape of route
        route_poly_shape = route_shape(start_coord,destination_coord)
        # get lat/ lon of route shape 
        polyline_coordinates = route_poly_shape['response']['route'][0]['shape']
        # calculating how many stations needed to be found during the trip.
        loops_static = round((trip_length_in_m/range_of_car))
        # delete every second shape several times to reduce size until size > 4700 characters
        if trip_length_in_m < 600000:
            while len(polyline_coordinates) > 160:
                print('polypunkte löschen 1')
                del polyline_coordinates[::2]
        else:
            while len(polyline_coordinates) > 220:
                print('polypunkte löschen 2')
                del polyline_coordinates[::2]
        print('löschen beendet')
        print("länge polyline coords " + str(len(polyline_coordinates)))
        if trip_length_in_m > 600000:
            corridor_width = 7000
        incr = int(len(polyline_coordinates)/loops_static)
        if incr == len(polyline_coordinates):
            incr = int(incr*(range_of_car/trip_length_in_m))
        stations_coordinates = []
        poly_start = start_coord
        c = incr
        reverse = False
        stations_coordinates = get_station_list(poly_start,polyline_coordinates[c],stations_coordinates,corridor_width,size_of_results,reverse)
        reverse = True
        stations_coordinates = get_station_list(poly_start,polyline_coordinates[c],stations_coordinates,corridor_width,size_of_results,reverse)
        poly_start = polyline_coordinates[c]
        j = (int(trip_length_in_m/range_of_car))-1
        k= 1
        station_position = 0
        while k <= j:
            c += incr
            if c >= len(polyline_coordinates):
                c = (len(polyline_coordinates)-1)
            reverse = False
            stations_coordinates = get_station_list(poly_start,polyline_coordinates[c],stations_coordinates,corridor_width,size_of_results,reverse)
            poly_start = polyline_coordinates[c]
            k +=1
        reverse = False
        stations_coordinates = get_station_list(poly_start,polyline_coordinates[-1],stations_coordinates,corridor_width,size_of_results,reverse)
        reverse = True
        stations_coordinates = get_station_list(poly_start,polyline_coordinates[-1],stations_coordinates,corridor_width,size_of_results,reverse)
        ###############
        # end of station collecting
        ################
        first_polyline_point = (int((len(polyline_coordinates))/loops_static))
        if first_polyline_point >= len(polyline_coordinates):
            first_polyline_point = int(len(polyline_coordinates))-10            
        a = 1
        station_start = start_coord
        whole_dist = 0
        charged = False
        loops_dyn = loops_static
        while a <= loops_dyn:
            if a == 1 and percentage_range_at_start < 1 and start_range < trip_length_in_m:
                loops3 = round(((trip_length_in_m-start_range)/range_of_car))
                if loops_dyn == loops3:
                    print("no more loops_dyn needed")
                if loops3 < loops_dyn:
                    loops_dyn = loops3
                range_of_car = start_range
            if a >1 and percentage_range_at_start < 1 and charged == False:
                dist_to_dest = trip_length(station_position,destination_coord)
                loops2 = round((dist_to_dest/real_range))
                if loops2 ==1:
                    print("no more loops_dyn needed")
                    range_of_car = int(real_range*0.8)
                if loops2 >1:
                    loops_dyn += loops2-1
                    range_of_car = int(real_range*0.8)
                charged = True
            if a >= 1 and percentage_range_at_start == 1: 
               range_of_car = int(real_range*0.8) 
            print('berechnung startet für loop ' + str(a))
            found = False
            while found == False:
                route_to_polyline_point_length_in_m = trip_length(station_start,polyline_coordinates[first_polyline_point])
                print("lenghth to poly point = " + str(route_to_polyline_point_length_in_m))
                print("fpp = " + str(first_polyline_point))                    
                if route_to_polyline_point_length_in_m > range_of_car*1.04:
                    factor_1 = range_of_car/route_to_polyline_point_length_in_m
                    #range_between_old_and_new = first_polyline_point - old_polyline_point
                    #add = int(range_between_old_and_new * factor_1)
                    #first_polyline_point = old_polyline_point + add
                    first_polyline_point = int(first_polyline_point *factor_1)
                    if first_polyline_point < old_polyline_point:
                        first_polyline_point = old_polyline_point
                else:
                    if route_to_polyline_point_length_in_m > (range_of_car*0.96) and route_to_polyline_point_length_in_m <= (range_of_car*1.04):
                        found = True
                    else:
                        h = True
                        while route_to_polyline_point_length_in_m < range_of_car and h == True:
                            print("route zu polypoint zu kurz ")
                            first_polyline_point += 8
                            if first_polyline_point > len(polyline_coordinates)-1:
                                first_polyline_point = len(polyline_coordinates)-1
                                h = False
                            route_to_polyline_point_length_in_m = trip_length(station_start,polyline_coordinates[first_polyline_point])
                            print("lenghth to poly point = " + str(route_to_polyline_point_length_in_m))
                        if h == True: 
                            first_polyline_point -= 8
                            found = True
                        else:
                            found = True
            print("found polypoint = " + str(first_polyline_point))
            print("polyline point gefunden")
            #get the calculated polyline point
            first_found_polypoint = polyline_coordinates[first_polyline_point]
            # calculate distances from polyline point to all stations along route, take the nearest station
            distances_station_from_found_polypoint = []
            for z in range(len(stations_coordinates)):
                dist = geopy.distance.distance(stations_coordinates[z], first_found_polypoint).km
                distances_station_from_found_polypoint.append(dist)
            stations_coordinates_with_distances_station_from_found_polypoint = pd.DataFrame({'distances_station_from_found_polypoint': distances_station_from_found_polypoint,'stations_coordinates': stations_coordinates})
            row_of_station = stations_coordinates_with_distances_station_from_found_polypoint['distances_station_from_found_polypoint'].idxmin()
            print("station_  row = " + str(row_of_station) + "of " + str(len(stations_coordinates)))
            station_position = stations_coordinates_with_distances_station_from_found_polypoint.at[row_of_station,'stations_coordinates']
            # get data from station
            #station_openingHours = stations_along_route['results']['items'][row_of_station]['openingHours']['text']
            #station_title = stations_along_route['results']['items'][row_of_station]['title']
            dist_to_station = trip_length(station_start,station_position)
            print("distanz zur gefundene station = " + str(dist_to_station))
            while dist_to_station > (range_of_car*1.04):
                print('distanz doch noch zu gross')
                row_of_station -= 1
                print("new row = " + str(row_of_station))
                station_position = stations_coordinates_with_distances_station_from_found_polypoint.at[row_of_station,'stations_coordinates']
                print(station_position)
                dist_to_station = trip_length(station_start,station_position)
                print("new dist to station : " + str(dist_to_station))
            list_of_waypoints.append(station_position)
            station_start = station_position
            old_polyline_point = first_polyline_point
            print('old_polyline_point = ' + str(old_polyline_point))
            first_polyline_point += (int((len(polyline_coordinates)/loops_static)))
            if first_polyline_point >= len(polyline_coordinates):
                first_polyline_point = (len(polyline_coordinates)-1)
            stations_coordinates_with_distances_station_from_found_polypoint = []
            row_of_station = 0
            print('next first_polyline_point = ' + str(first_polyline_point))
            whole_dist += dist_to_station
            if a == loops_dyn and whole_dist < (trip_length_in_m-range_of_car):
                loops_dyn +=1
            if dist_to_station == 0:
                a = loops_dyn+1
                list_of_waypoints.append(station_position)
            dist_to_dest_2 = trip_length(station_position,destination_coord)
            print('dist to dest  = ' + str(dist_to_dest_2))
            run = False
            dist_to_dest_4 = 0            
            if dist_to_dest_2 == dist_to_dest_4 and run == True:
                a = loops_dyn+1
            if dist_to_dest_2 > range_of_car and a == loops_dyn:
                loops_dyn +=1
            a += 1    
            if dist_to_dest_2 < range_of_car:
                a = loops_dyn+1
            dist_to_dest_4 = dist_to_dest_2
            run = True
    else: 
        print("no need to carge during this trip. The Battery of the car will last")
    list_of_waypoints.append(destination_coord)
    if (len(list_of_waypoints) == len(set(list_of_waypoints)))==False:
        list_of_waypoints = []
    print("--- %s seconds ---" % (time.time() - start_time))
    return list_of_waypoints
#################################################################################
# TEST SECTION
##########################a#######################################################
start = 'Berlin' 
destination = 'Rom'
range_of_car = 161000
percentage_range_at_start = 0.2
list_of_waypoints = complete_route(start, destination, range_of_car, percentage_range_at_start)
url = ''
for x in range(len(list_of_waypoints)):
    url += str(list_of_waypoints[x]) + '/'
google = 'https://www.google.com/maps/dir/' + url
print(google)