from django.shortcuts import render
import requests
import pandas as pd
from django.http import JsonResponse
from django.http import HttpResponse
import json
#import ajax_handler


def index(request):
    cars_frame = pd.read_csv("C:/Users/David/Desktop/eCars.csv", sep=';')
    cars_list = cars_frame["Car"].tolist()
    return render(request, 'routing/index.html', {"cars_list": cars_list})


def routing(request):
    return render(request, 'routing/routing.html')


def team(request):
    city = ''
    form = ''
    if request.method == 'POST':
        city = request.POST.get('city', 'leer')
        form = request.POST.get('city2', 'leer')
    return render(request, 'routing/team.html', {'car': [city, form, 'Toyotoa', ],
                                                 'style': ['Fast', 'Average', 'Slow', ],
                                                 'form': form, 'city': city, })


def algorithm(request):
    # Get list of all cars from csv
    cars_frame = pd.read_csv("C:/Users/David/Desktop/eCars.csv", sep=';')
    cars_list = cars_frame["Car"].tolist()
    return render(request, 'routing/algorithm.html', {"cars_list": cars_list})


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



        #distance = direction_json['legs_distance']
        #waypoints = waypoints_x['legs_distance']

        #resp_dict = json.loads(resp_str)

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


#
def get_direction_data(start, destination):
    api_key = 'AIzaSyAonN5q0C_6Vlvm8VGIWPd-vl43vjJqca0'
    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
    waypoint_array = ["Frankfurt", "München", "Paris"]

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