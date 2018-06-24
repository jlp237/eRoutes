import mysql.connector
import pandas as pd
from django.http import JsonResponse



def get_car_data(request):
    if request.method == 'GET':
        car = request.GET.get('car_model')

        connection = mysql.connector.connect(user='dsteiner', password='eMobility2018DS',
                                             host='mobility.f4.htw-berlin.de',
                                             database='electric_vehicles', buffered=True)

        print("--AJAX request--")
        print("selected car: " + car)

        # get all car data from database for selected car
        try:
            cursor = connection.cursor()
            selectString = ("select battery_capacity_kwh, charge_port,"
                            " charge_power, comb_cold_weather, comb_mild_weather,"
                            " fastcharge_port, range_km, acceleration, top_speed, total_power from vehicles where name = '" + car + "'")
            cursor.execute(selectString)
            result = cursor.fetchone()
            carDataRaw = pd.DataFrame(list(result))
            carData = carDataRaw.transpose()
            carData.columns = ["battery_capacity_kwh", "charge_port", "charge_power",
                               "comb_cold_weather", "comb_mild_weather",
                               "fastcharge_port", "range_km", "acceleration", "top_speed", "total_power"]

            data = {
                'car_range': round(carData["range_km"][0],0),
                'car_battery':  carData["battery_capacity_kwh"][0],
                'car_acceleration':  carData["acceleration"][0],
                'car_speed':  carData["top_speed"][0],
                'car_power':  carData["total_power"][0],
            }
            return JsonResponse(data)

        finally:
            connection.commit()
            connection.close()



#cars_frame = pd.read_csv('/static/csv/eCars.csv', sep=';')

def get_car_data_csv(request):
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