import requests
from .charging_stations import *


#100 km standart range ; changes when car is selected
car_range_num = 200000

def get_direction_data(start, destination):
    api_key = 'AIzaSyAonN5q0C_6Vlvm8VGIWPd-vl43vjJqca0'
    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
    #waypoint_array = ["Frankfurt", "München", "Paris"]
    waypoints = ""

    range_of_car = car_range_num
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