from django.shortcuts import render
from datetime import timedelta
import pandas as pd

from .api_handler import *
from .ajax_handler import *
from .charging_stations import *
from .charging_station_prices import *
from .direction_data import *
from .car_data import *


def index(request):
    # Get list of all cars from csv
    cars_frame = pd.read_csv("C:/Users/David/Desktop/eCars.csv", sep=';')
    cars_list = cars_frame["Car"].tolist()
    return render(request, 'routing/index.html', {"cars_list": cars_list})


def team(request):
    return render(request, 'routing/team.html')


def contact(request):
    return render(request, 'routing/contact.html')


def algorithm(request):
    return render(request, 'routing/algorithm.html')


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


def output(request):
    if request.method == 'POST':
        start = request.POST.get('start', 'leer')
        destination = request.POST.get('destination', 'leer')
        car = request.POST.get('car', 'leer')
        driving_style = request.POST.get('driving_style', 'leer')
        battery_status = request.POST.get('battery_status', 'leer')


        # get car data from database: Input: car
        #price = (getStationPrice(50.20286, 11.776482))
        price = 50

        route_json = get_direction_data(start, destination, car, battery_status, driving_style)

        # Waypoints string
        waypoints = route_json['waypoints_return']


        # Routing URL
        url = route_json['google_url']
        car_range = round(route_json['range_of_car'], 0) / 1000

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
        driving_time_min = round(sum(driving_time_array) / 60, 0)

        # build string of charging station data
        charging_station = route_json['routes'][0]['legs']
        all_waypoints_string = []
        for i in range(len(charging_station)-1):
            address2 = charging_station[i]['end_address']
            distance2 = charging_station[i]['distance']['text']
            duration2 = charging_station[i]['duration']['text']
            text = 'Provider:\n' + address2 + '\n' + distance2 + '\n' + duration2 + '\n' + 'Charging Type:'
            all_waypoints_string.append(text)

        # total time, waiting time, charging time
        count_stations = len(charging_station)-1
        charging_time_min = 30 * count_stations
        waiting_time_min = 2 * count_stations
        total_time = min_to_hour(driving_time_min + charging_time_min + waiting_time_min)
        driving_time = min_to_hour(driving_time_min)
        charging_time = min_to_hour(charging_time_min)
        waiting_time = min_to_hour(waiting_time_min)

        # Weather and geo api call
        temperature_start = get_weather_start(start)
        temperature_destination = get_weather_destination(destination)
        geo_coordinates = get_geo_data(start)

        # Calculate Overview Data (total cost, money saved, distance)
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
                                                       'all_waypoints_string': all_waypoints_string,
                                                       'charging_time': charging_time,
                                                       'waiting_time': waiting_time,
                                                       'total_time': total_time,
                                                       'price': price,
                                                       'url': url,
                                                       'car_range': car_range,
                                                       })
    else:
        return render(request, 'routing/output.html')


def min_to_hour(min):
    return str(timedelta(minutes=min))[:-3]
