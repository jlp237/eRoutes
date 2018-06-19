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


def complete_route(start, destination, range_of_car, battery_status):

    # set start Range (0-100% from full battery)
    start_range = int(battery_status)/100 * range_of_car
    print("Start Range: " + str(start_range))

    # set corridor width and result size then parse shape to corridor api and get the stations along the route
    range_of_car = int(range_of_car*0.96)
    corridor_width = 3000
    size_of_results = 300
    old_polyline_point = 0
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
        polyline_coordinates = route_poly_shape['response']['route'][0]['shape']
        # calculating how many stations needed to be found during the trip.
        loops = round((trip_length_in_m/range_of_car))
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
        if len(polyline_coordinates) < 200 and trip_length_in_m > 600000:
            corridor_width = 5000
        incr = int(len(polyline_coordinates)/loops)
        c= 0
        stations_coordinates = []
        g = round((trip_length_in_m/range_of_car)+0.5)
        f= 0
        poly_start = start_coord
        while f < g:
            c += incr
            if c >= len(polyline_coordinates):
                c = len(polyline_coordinates)-1
            route_poly_shape = route_shape(poly_start, polyline_coordinates[c])
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
            stations_coordinates.extend(temp_stations)
            stations_coordinates = list(dict.fromkeys(stations_coordinates))
            print("neue stationsliste stationsanzahl = " + str(len(stations_coordinates)))
            ########################
            route_poly_shape = route_shape(polyline_coordinates[c],poly_start)
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
            temp_stations.reverse()
            stations_coordinates.extend(temp_stations)
            stations_coordinates = list(dict.fromkeys(stations_coordinates))
            print("neue stationsliste stationsanzahl = " + str(len(stations_coordinates)))
            f += 1
            poly_start = polyline_coordinates[c]
        ###############
        # end of station collecting
        ################
        first_polyline_point = (int((len(polyline_coordinates))/loops))
        if first_polyline_point >= len(polyline_coordinates):
            first_polyline_point = int(len(polyline_coordinates))-10
        a = 1
        station_start = start_coord
        while a <= loops:
            print('berechnung startet für loop ' + str(a))
            found = False
            while found == False:
                route = here_route(station_start,polyline_coordinates[first_polyline_point])
                route_to_polyline_point_length_in_m = (route['response']['route'][0]['summary']['distance'])
                print("lenghth to poly point = " + str(route_to_polyline_point_length_in_m))
                print("fpp = " + str(first_polyline_point))
                if route_to_polyline_point_length_in_m > range_of_car*1.04:
                    factor_1 = range_of_car/route_to_polyline_point_length_in_m
                    #range_between_old_and_new = first_polyline_point - old_polyline_point
                    #add = int(range_between_old_and_new * factor_1)
                    #first_polyline_point = old_polyline_point + add
                    first_polyline_point = int(first_polyline_point *factor_1)
                else:
                    if route_to_polyline_point_length_in_m > (range_of_car*0.96) and route_to_polyline_point_length_in_m <= (range_of_car*1.04):
                        found = True
                    else:
                        h = True
                        while route_to_polyline_point_length_in_m < range_of_car and h == True:
                            print("route zu station zu kurz ")
                            first_polyline_point += 4
                            if first_polyline_point > len(polyline_coordinates)-1:
                                first_polyline_point = len(polyline_coordinates)-1
                                h = False
                            route = here_route(station_start,polyline_coordinates[first_polyline_point])
                            route_to_polyline_point_length_in_m = (route['response']['route'][0]['summary']['distance'])
                            print("lenghth to poly point = " + str(route_to_polyline_point_length_in_m))
                        if h == True:
                            first_polyline_point -= 4
                            found = True
                        else:
                            found = True
            print("found polypoint = " + str(first_polyline_point))
            print("station gefunden")
            #get the calculated polyline point
            first_found_polypoint = polyline_coordinates[first_polyline_point]
            # calculate distances from polyline point to all stations along route, take the nearest station
            distances_station_from_found_polypoint = []
            for z in range(len(stations_coordinates)):
                dist = geopy.distance.distance(stations_coordinates[z], first_found_polypoint).km
                distances_station_from_found_polypoint.append(dist)
            stations_coordinates_with_distances_station_from_found_polypoint = pd.DataFrame({'distances_station_from_found_polypoint': distances_station_from_found_polypoint,'stations_coordinates': stations_coordinates})
            row_of_station = stations_coordinates_with_distances_station_from_found_polypoint['distances_station_from_found_polypoint'].idxmin()
            station_position = stations_coordinates_with_distances_station_from_found_polypoint.at[row_of_station,'stations_coordinates']
            # get data from station
            #station_openingHours = stations_along_route['results']['items'][row_of_station]['openingHours']['text']
            #station_title = stations_along_route['results']['items'][row_of_station]['title']
            route = here_route(station_start,station_position)
            dist_to_station = (route['response']['route'][0]['summary']['distance'])
            print("distanz zur gefundene station = " + str(dist_to_station))
            while dist_to_station > (range_of_car*1.04):
                print('distanz doch noch zu gross')
                row_of_station -= 1
                print("new row = " + str(row_of_station))
                station_position = stations_coordinates_with_distances_station_from_found_polypoint.at[row_of_station,'stations_coordinates']
                print(station_position)
                route = here_route(station_start,station_position)
                dist_to_station = (route['response']['route'][0]['summary']['distance'])
                print("new dist to station : " + str(dist_to_station))
            list_of_waypoints.append(station_position)
            station_start = station_position
            old_polyline_point = first_polyline_point
            print('old_polyline_point = ' + str(old_polyline_point))
            first_polyline_point += (int((len(polyline_coordinates)/loops)))
            if first_polyline_point >= len(polyline_coordinates):
                first_polyline_point = (len(polyline_coordinates)-1)
            stations_coordinates_with_distances_station_from_found_polypoint = []
            row_of_station = 0
            print('next first_polyline_point = ' + str(first_polyline_point))
            a += 1
    else:
        print("no need to charge during this trip. The Battery of the car will last")
    list_of_waypoints.append(destination_coord)
    if len(list_of_waypoints) ==2:
        list_of_waypoints = []
    if list_of_waypoints[1]== list_of_waypoints[2]:
        list_of_waypoints = []
        error = "error"
        list_of_waypoints.append(error)
    print("--- %s seconds ---" % (time.time() - start_time))
    return list_of_waypoints