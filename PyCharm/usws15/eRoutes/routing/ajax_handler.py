import pandas as pd
from django.http import JsonResponse
from django.http import HttpResponse
import json

from .ajax_handler import *

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

        range_string = car_range[:-2]
        global car_range_num
        car_range_num = int(int(range_string) * 1.6)

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