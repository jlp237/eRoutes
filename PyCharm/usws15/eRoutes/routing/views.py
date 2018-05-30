from django.shortcuts import render
import requests
import pandas as pd
from django.http import JsonResponse
from django.http import HttpResponse
import json
import geopy.distance
#import ajax_handler


def index(request):
    # Get list of all cars from csv
    cars_frame = pd.read_csv("C:/Users/David/Desktop/eCars.csv", sep=';')
    cars_list = cars_frame["Car"].tolist()
    return render(request, 'routing/index.html', {"cars_list": cars_list})


def routing(request):
    return render(request, 'routing/routing.html')


def team(request):
    return render()


def algorithm(request):
    return render()


def search(request):
    if 'start' in request.POST:
        message = 'You searched for: %r' % request.POST['start']
    else:
        message = 'You submitted an empty form.'
    return render(request, message)


def my_view(request):
    context = {}
    if request.method == 'POST':
        city = request.POST.get('city', 'leer')
        context['temperature'] = city
    render(request, 'routing/team.html', context)



###### OUTPUT #######
def output(request):
    if request.method == 'POST':
        start = request.POST.get('start', 'leer')
        destination = request.POST.get('destination', 'leer')
        car = request.POST.get('car', 'leer')
        driving_style = request.POST.get('driving_style', 'leer')
        battery_status = request.POST.get('battery_status', 'leer')


        route_json = get_direction_data(start, destination)

        # Waypoints string
        waypoints = route_json['waypoints_return']

        # Total Distance
        distance_array = []
        for i in range(len(route_json['routes'][0]['legs'])):
            charging_station = route_json['routes'][0]['legs'][i]['distance']['value']
            distance_array.append(charging_station)
        distance = sum(distance_array)

        # Driving Time
        driving_time_array = []
        for i in range(len(route_json['routes'][0]['legs'])):
            charging_station = route_json['routes'][0]['legs'][i]['duration']['value']
            driving_time_array.append(charging_station)
        driving_time = round(sum(driving_time_array) / 3600, 2)



        temperature_start = get_weather_start(start)
        temperature_destination = get_weather_destination(destination)
        geo_coordinates = get_geo_data(start)

        total_cost = round((distance / 1000) * 1.6 * 0.025, 2)
        money_saved = round(((distance / 1000) * 1.6 * 0.13) - total_cost, 2)
        distance = round(distance / 1000, 1)

        return render(request, 'routing/output.html', {'start': start,
                                                       'destination': destination,
                                                       'car': car,
                                                       'driving_style': driving_style,
                                                       'battery_status': battery_status,
                                                       'temperature_start': temperature_start,
                                                       'temperature_destination': temperature_destination,
                                                       'geo_coordinates': geo_coordinates,
                                                       'distance': distance,
                                                       'total_cost': total_cost,
                                                       'money_saved': money_saved,
                                                       'waypoints': waypoints,
                                                       'driving_time': driving_time,
                                                       })
    else:
        return render(request, 'routing/output.html')


######################## APIs #######################


def get_weather_start(start):
    api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=31d7b827392ab249e871954306d44d04&q='
    url = api_address + start
    json_data = requests.get(url).json()
    kelvin = json_data['main']['temp']
    temperature_start = round(kelvin - 273.15, 0)
    return temperature_start


def get_weather_destination(destination):
    api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=31d7b827392ab249e871954306d44d04&q='
    url = api_address + destination
    json_data = requests.get(url).json()
    kelvin = json_data['main']['temp']
    temperature_destination = round(kelvin - 273.15, 0)
    return temperature_destination


def get_geo_data(start):
    api_key = 'AIzaSyCSLetZcqVMjiQMdfR7mudMe5bwzWIYzqo'
    location = start
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + location + '&key=' + api_key
    json_data = requests.get(url).json()
    geo_data = json_data['results'][0]['geometry']['location']
    return geo_data


def get_direction_data(start, destination):
    api_key = 'AIzaSyAonN5q0C_6Vlvm8VGIWPd-vl43vjJqca0'
    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
    #waypoint_array = ["Frankfurt", "München", "Paris"]
    waypoints = ""

    range_of_car = 250000
    waypoint = complete_route(start, destination, range_of_car)
    if len(waypoint) > 2:
        waypoint_array = waypoint[1:-1]

        # create waypoints strings
        waypoint_counter = 1
        waypoint_map_string = ""
        waypoint_request_string = ""
        for waypoint in waypoint_array:
            waypoint_map_string += 'location' + str(waypoint_counter) + '=' + waypoint + '&'
            waypoint_request_string += waypoint + '|'
            waypoint_counter += 1
        waypoints_return = waypoint_map_string[:-1]
        waypoints = waypoint_request_string[:-1]

    # make request for routing json
    nav_request = 'origin={}&destination={}&waypoints={}&key={}'.format(start, destination, waypoints, api_key)
    url = endpoint + nav_request
    json_data = requests.get(url).json()
    routes = json_data['routes']

    # prepare return json
    data = {
        'routes': routes,
        'waypoints_return': waypoints_return,
    }
    return data


######################## AJAX HANDLER #######################


def get_car_data(request):
    if request.method == 'GET':
        car_model = request.GET.get('car_model')
        cars_frame = pd.read_csv("C:/Users/David/Desktop/eCars.csv", sep=';')
        frame2 = cars_frame.set_index('Car', drop=True, append=False, inplace=False, verify_integrity=False)

        car_range = (frame2.loc[car_model]['Range'])
        car_battery = (frame2.loc[car_model]['Battery Capacity'])
        car_acceleration = (frame2.loc[car_model]['Acceleration 0 - 62 mph'])
        car_speed = (frame2.loc[car_model]['Top Speed'])
        car_power = (frame2.loc[car_model]['Total Power'])

        data = {
            'car_range': car_range,
            'car_battery': car_battery,
            'car_acceleration': car_acceleration,
            'car_speed': car_speed,
            'car_power': car_power
        }
        return JsonResponse(data)

    else:
        return HttpResponse("ERROR get_car_data")


######################## ALGORITHM #######################

# 1. all neccessary functions are listed here:

# a geocoder that translates an address or given place from a string into coordinates

def geocoder(place):
    r = requests.get(
        'https://geocoder.cit.api.here.com/6.2/geocode.json?app_id=jccZtyShstzovgbVxAJn&app_code=5ezWDCQaAJYiXldHFRV6gA&searchtext=' + place)
    place_geo = r.json()
    latitude = place_geo['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]['Latitude']
    longitude = place_geo['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]['Longitude']
    coordinates = str(latitude) + ',' + str(longitude)
    return coordinates


# an api request that returns a route between two given waypoints

def here_route(start_coord, destination_coord):
    r = requests.get(
        'https://route.cit.api.here.com/routing/7.2/calculateroute.json?app_id=jccZtyShstzovgbVxAJn&app_code=5ezWDCQaAJYiXldHFRV6gA&waypoint0=' + start_coord + '&waypoint1=' + destination_coord + '&mode=fastest;car;traffic:disabled')
    route = r.json()
    return route


# an api request that returns the shape of a route between two given waypoints as an object with many many coordinates

def route_shape(start_coord, destination_coord):
    r = requests.get(
        'https://route.api.here.com/routing/7.2/calculateroute.json?waypoint0=' + start_coord + '&waypoint1=' + destination_coord + '&mode=fastest;car;traffic:enabled&routeattributes=shape&app_id=jccZtyShstzovgbVxAJn&app_code=5ezWDCQaAJYiXldHFRV6gA')
    route = r.json()
    return route


# an api request that returns all stations along a route in specified corridor around the route

def get_stations_along_route(string_route_shapes, corridor_width, size_of_results):
    r = requests.get(
        'https://places.cit.api.here.com/places/v1/browse/by-corridor?app_id=jccZtyShstzovgbVxAJn&app_code=5ezWDCQaAJYiXldHFRV6gA&route=' + string_route_shapes + ';w=' + str(
            corridor_width) + '&cat=ev-charging-station&size=' + str(size_of_results))
    stations = r.json()
    return stations


def complete_route(start, destination, range_of_car):
    # api call for geocoding strings into coordinates
    start_coord = geocoder(start)
    destination_coord = geocoder(destination)
    list_of_waypoints = []
    list_of_waypoints.append(start_coord)
    # api call for route calculation
    print("1")
    route = here_route(start_coord, destination_coord)
    trip_length_in_m = (route['response']['route'][0]['summary']['distance'])
    if trip_length_in_m > range_of_car:
        # api call for getting the shape of route
        route_poly_shape = route_shape(start_coord, destination_coord)
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
        stations_along_route = get_stations_along_route(string_route_shape, corridor_width, size_of_results)
        # create list with all coordinates of the found stations
        stations_coordinates = []
        for x in range(len(stations_along_route['results']['items'])):
            lat_1 = stations_along_route['results']['items'][x]['position'][0]
            lon_1 = stations_along_route['results']['items'][x]['position'][1]
            stations_coordinates.append(str(lat_1) + ',' + str(lon_1))
        # calculating how many stations needed to be found during the trip.
        print("3")
        loops = int((trip_length_in_m / range_of_car))
        # select the first guess for a polyline point by dividing the list of polyline points by the rounded number of loops
        first_polyline_point = int((len(polyline_coordinates)) / loops)
        # loop for all stations during trip
        a = 1
        print("4")
        while a <= (loops):
            distance_polypoint_to_start = 0
            # loop to find polypoint on route after range of car
            # calculate route between start and polyline point
            print(first_polyline_point)
            route = here_route(start_coord, polyline_coordinates[first_polyline_point])
            # get distance
            route_to_polyline_point_length_in_m = (route['response']['route'][0]['summary']['distance'])
            # raise counter by distance of route
            distance_polypoint_to_start = route_to_polyline_point_length_in_m
            print(distance_polypoint_to_start)

            if distance_polypoint_to_start >= range_of_car:
                first_polyline_point = int(first_polyline_point / 2)
                distance_polypoint_to_start = 0
                print(distance_polypoint_to_start)

                print("if")
                print(first_polyline_point)
                # get route
                route = here_route(start_coord, polyline_coordinates[first_polyline_point])
                # get distance
                route_to_polyline_point_length_in_m = (route['response']['route'][0]['summary']['distance'])
                # raise counter by distance of route
                distance_polypoint_to_start = route_to_polyline_point_length_in_m

                first_polyline_point += 2


            else:
                # raise counter for next polyline point
                first_polyline_point += 2
                print("else")
                print(first_polyline_point)
            while distance_polypoint_to_start <= range_of_car and first_polyline_point <= int(
                    len(polyline_coordinates)):
                route = here_route(start_coord, polyline_coordinates[first_polyline_point])
                # get distance
                route_to_polyline_point_length_in_m = (route['response']['route'][0]['summary']['distance'])
                # raise counter by distance of route
                distance_polypoint_to_start = route_to_polyline_point_length_in_m
                first_polyline_point += 2
                print("while")
                print(first_polyline_point)
                print(distance_polypoint_to_start)
            # get the calculated polyline point
            first_found_polypoint = polyline_coordinates[first_polyline_point]
            # calculate distances from polyline point to all stations along route, take the nearest station
            print("5")
            distances_station_from_found_polypoint = []
            for z in range(len(stations_coordinates)):
                coords_1 = stations_coordinates[z]
                coords_2 = first_found_polypoint
                dist = geopy.distance.distance(coords_1, coords_2).km
                distances_station_from_found_polypoint.append(dist)
            stations_coordinates_with_distances_station_from_found_polypoint = pd.DataFrame(
                {'distances_station_from_found_polypoint': distances_station_from_found_polypoint,
                 'stations_coordinates': stations_coordinates})
            row_of_station = stations_coordinates_with_distances_station_from_found_polypoint[
                'distances_station_from_found_polypoint'].idxmin()

            print("6")
            # get data from station
            # station_openingHours = stations_along_route['results']['items'][row_of_station]['openingHours']['text']
            station_position = str(stations_along_route['results']['items'][row_of_station]['position'][0]) + ',' + str(
                stations_along_route['results']['items'][row_of_station]['position'][1])
            # station_title = stations_along_route['results']['items'][row_of_station]['title']
            list_of_waypoints.append(station_position)
            start_coord = station_position
            print(first_polyline_point)
            print(a)
            first_polyline_point = int(first_polyline_point * 1.5)
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

