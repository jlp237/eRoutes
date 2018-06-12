import requests
from .charging_stations import *
#from car_data import *


#100 km standart range ; changes when car is selected


def get_direction_data(start, destination, car):
    api_key = 'AIzaSyAonN5q0C_6Vlvm8VGIWPd-vl43vjJqca0'
    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
    waypoints = ""

    # get all the data about selected car from database
    range_of_car = get_car_data(car)



    # get list of best charging stations along the way
    waypoint = complete_route(start, destination, range_of_car)
    if len(waypoint) > 2:
        waypoint_array = waypoint[1:-1]

        url = ''
        for x in range(len(waypoint)):
            url += str(waypoint[x]) + '/'
        google_url = 'https://www.google.com/maps/dir/' + url


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
        'google_url': google_url,
    }
    return data


def get_car_data(car):
    # PLACEHOLDER DB QUERY
    car_range_num = 200000
    return car_range_num
