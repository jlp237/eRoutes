import requests
from .charging_stations import *
from .api_handler import *
from .charging_station_prices import *
#from car_data import *


def get_direction_data(start, destination, car, battery_status, driving_style):
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
    waypoint = complete_route(start, destination, range_of_car, battery_status)
    waypoint_array = []

    charging_station_data = get_station_data(waypoint)


    if len(waypoint) > 2:
        waypoint_array = waypoint[1:-1]

    #get price for charging station and charging provider
    #waypoint_prices =


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
        'range_of_car': range_of_car,
        'charging_station_data': charging_station_data,
    }
    return data


import mysql.connector
import pandas as pd


def get_car_data(car, start):
    connection = mysql.connector.connect(user='dsteiner', password='eMobility2018DS',
                                         host='mobility.f4.htw-berlin.de',
                                         database='electric_vehicles', buffered=True)

    # get range for cold weather if temperature is less than 10 degree celsius
    temperature = get_weather_start(start)
    if temperature < 10:
        value = 'comb_cold_weather'
    else:
        value = 'comb_mild_weather'


    print("range" +value)
    print("car" + car)

    # get all car data from database for selected car
    try:
        cursor = connection.cursor()
        selectString = ("select battery_capacity_kwh, charge_port,"
                        " charge_power, comb_cold_weather, comb_mild_weather,"
                        " fastcharge_port, range_km from vehicles where name = '" + car + "'")
        cursor.execute(selectString)
        result = cursor.fetchone()
        carDataRaw = pd.DataFrame(list(result))
        carData = carDataRaw.transpose()
        carData.columns = ["battery_capacity_kwh", "charge_port", "charge_power",
                           "comb_cold_weather", "comb_mild_weather",
                           "fastcharge_port", "range_km"]
        return (carData[value][0])
    finally:
        connection.commit()
        connection.close()


