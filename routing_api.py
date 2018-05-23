# -*- coding: utf-8 -*-
"""
Created on Tue May 22 13:43:29 2018

@author: David
"""

#Routing API
#https://maps.googleapis.com/maps/api/directions/json?origin=New+York,+NY&destination=Boston,+MA&waypoints=optimize:true|Providence,+RI|Hartford,+CT&key='
import json
import requests 

api_key = 'AIzaSyAonN5q0C_6Vlvm8VGIWPd-vl43vjJqca0'
endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
origin = 'Berlin'
destination = 'Hamburg'

nav_request = 'origin={}&destination={}&key={}'.format(origin,destination,api_key)
url = endpoint + nav_request
json_data = requests.get(url).json()

routes = json_data['routes']
legs = routes[0]['legs']
legs_distance = legs[0]['distance']['value']