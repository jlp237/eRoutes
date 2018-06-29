from .views import *
import webbrowser
from .car_specs_data import *


# this method builds the url for google maps and adjusts the range to driving style
def get_direction_data(start, destination, car, battery_status, driving_style):

    try:

        api_key = 'AIzaSyAonN5q0C_6Vlvm8VGIWPd-vl43vjJqca0'
        endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
        waypoints = ""

        # get all data of selected car from database
        range_of_car = get_car_data(car, start)
        range_of_car = range_of_car * 1000

        print("Driving Style: " + driving_style)
        print("Normal Range: " + str(range_of_car))

        if driving_style == "Fast":
            range_of_car = range_of_car * 0.8
        elif driving_style == "Slow":
            range_of_car = range_of_car * 1.2

        print("Adjusted Range: " + str(range_of_car))

        # get list of best charging stations along the way / Class:  Charging_stations.py
        percentage_range_at_start = int(battery_status) / 100
        waypoint = complete_route(start, destination, range_of_car, percentage_range_at_start)
        waypoint_array = []

        charging_station_data = get_station_data(waypoint)
        # render error html if list is empty
        if len(waypoint) == 0:
            print("Trip not possible with selected specs : Not enough charging stations")
            waypoints_return = "not_enough_stations_error"
            #webbrowser.open("/error/")
            data = {
                'waypoints_return': waypoints_return,
            }
            return data

        else:
            # add charging station at destination if trip doesnt contain charging sations
            if len(waypoint) <= 2:
                print("Trip contains no charging stations")
                waypoint.append(waypoint[-1])

            # delete start and end waypoint
            if len(waypoint) > 2:
                print("Trip contains charging stations")
                waypoint_array = waypoint[1:-1]

            url = ''
            for x in range(len(waypoint)):
                url += str(waypoint[x]) + '/'
            google_url = 'https://www.google.com/maps/dir/' + url


            # create waypoints strings
            waypoints_return = []
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
                'range_of_car': range_of_car,
                'charging_station_data': charging_station_data,
            }
            return data

    except:
        print("ERROR in direction_data")
        waypoints_return = "direction_data_error"

        data = {
            'waypoints_return': waypoints_return,
        }
        return data








