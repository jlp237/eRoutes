import requests


def get_weather_start(start):
    try:
        api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=31d7b827392ab249e871954306d44d04&q='
        url = api_address + start
        json_data = requests.get(url).json()
        kelvin = json_data['main']['temp']
        temperature_start = round(kelvin - 273.15, 0)
    except:
        temperature_start = 20

    return temperature_start


def get_weather_destination(destination):
    try:
        api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=31d7b827392ab249e871954306d44d04&q='
        url = api_address + destination
        json_data = requests.get(url).json()
        kelvin = json_data['main']['temp']
        temperature_destination = round(kelvin - 273.15, 0)
    except:
        temperature_destination = 20

    return temperature_destination


def get_geo_data(start):
    api_key = 'AIzaSyCSLetZcqVMjiQMdfR7mudMe5bwzWIYzqo'
    location = start
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + location + '&key=' + api_key
    json_data = requests.get(url).json()
    geo_data = json_data['results'][0]['geometry']['location']
    return geo_data


