import mysql.connector
import pandas as pd
from .api_handler import *


# this method returns the battery capacity or fastcahrging time of selected car
def getBatteryData(car, value):
    connection = mysql.connector.connect(user='dsteiner', password='eMobility2018DS',
                                         host='mobility.f4.htw-berlin.de',
                                         database='electric_vehicles', buffered=True)
    try:
        cursor = connection.cursor()
        selectString = ("select battery_capacity_kwh, fastcharge_time "
                        "from vehicles where name = '" + car + "'")
        cursor.execute(selectString)
        result = cursor.fetchone()
        carDataRaw = pd.DataFrame(list(result))
        carData = carDataRaw.transpose()
        carData.columns = ["battery_capacity_kwh", "fastcharge_time"]
        return(carData[value][0])
    finally:
        connection.commit()
        connection.close()


# this method gets the range of the car from the database, taken into consideration the outside temperature
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

    print("range" + value)
    print("car" + car)

    try:
        cursor = connection.cursor()
        selectString = ("select comb_cold_weather, comb_mild_weather,"
                        " range_km from vehicles where name = '" + car + "'")
        cursor.execute(selectString)
        result = cursor.fetchone()
        carDataRaw = pd.DataFrame(list(result))
        carData = carDataRaw.transpose()
        carData.columns = ["comb_cold_weather", "comb_mild_weather",
                           "range_km"]
        return (carData[value][0])
    finally:
        connection.commit()
        connection.close()