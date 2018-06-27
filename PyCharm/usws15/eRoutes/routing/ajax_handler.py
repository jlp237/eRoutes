import mysql.connector
import pandas as pd
from django.http import JsonResponse


# this method returns selected data from the database that will be used at the index page
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
