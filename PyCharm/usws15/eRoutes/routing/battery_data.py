import mysql.connector
import pandas as pd


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

