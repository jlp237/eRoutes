import json
import requests
import pandas as pd
import math
import mysql.connector


def get_connection():
    connection = mysql.connector.connect(user='tvancura', password='eMobility2018TV',
                                         host='mobility.f4.htw-berlin.de',
                                         database='stations', buffered=True)
    return connection


# get station prices by latitude and longitude
def get_station_price(lat, long):
    connection = get_connection()

    # searching stations in radius 0.001 around long and lat
    # first check via sql query: count number of results

    try:
        cursor = connection.cursor()
        selectString = ("select count(charging_per_kwh) from plugsurfing where "
                        "latitude > %s and latitude < %s "
                        "and longitude > %s and longitude < %s "
                        "and charging_per_kwh > 0.00")
        data = (lat - 0.0005, lat + 0.0005, long - 0.0005, long + 0.0005)
        cursor.execute(selectString, data)
        results = cursor.fetchone()

        # if there are results, return the exact price

        if (results[0] > 0):

            cursor2 = connection.cursor()
            selectString2 = ("select name, charging_per_kwh, type from plugsurfing where "
                             "latitude > %s and latitude < %s "
                             "and longitude > %s and longitude < %s "
                             "and charging_per_kwh > 0.00")
            data2 = (lat - 0.0005, lat + 0.0005, long - 0.0005, long + 0.0005)
            cursor2.execute(selectString2, data2)
            tmpResult2 = cursor2.fetchone()
            result2 = [tmpResult2[0], round(float(tmpResult2[1]), 2), tmpResult2[2]]
            return result2;

        # if there are no results, check the stations close to the
        # requested stations and return the average price
        # if radius of 2 geopoints around the requested station still
        # not delivers a specific price, select the avg price of a large range (20)

        else:
            cursor3 = connection.cursor()
            selectString3 = ("select name, avg(charging_per_kwh) from plugsurfing where "
                             "latitude > %s and latitude < %s "
                             "and longitude > %s and longitude < %s "
                             "and charging_per_kwh > 0")
            data3 = (lat - 20, lat + 20, long - 20, long + 20)
            cursor3.execute(selectString3, data3)
            tmpResult3 = cursor3.fetchone()
            result3 = [tmpResult3[0], round(tmpResult3[1], 2), '-']

            if(tmpResult3[1] > 0.01):
                return result3
            else:
                cursor4 = connection.cursor()
                selectString4 = ("select name, avg(charging_per_kwh) from plugsurfing where "
                                 "latitude > %s and latitude < %s "
                                 "and longitude > %s and longitude < %s "
                                 "and charging_per_kwh > 0")
                data4 = (lat - 10, lat + 10, long - 10, long + 10)
                cursor4.execute(selectString4, data4)
                tmpResult4 = cursor4.fetchone()
                result4 = [tmpResult4[0], round(tmpResult4[1], 2), '-']


    finally:
        connection.close()


# get station data for a list of specific geodata
def get_station_data(geodata):
    station_list = []
    stations_data = []

    for i in geodata:
        print("List append with value " + str(i))
        station_list.append(i.split(','))

    # search and return prices and charging_speed
    for i, j in station_list:
        station_data = get_station_price(float(i), float(j))
        stations_data.append([station_data[0], station_data[1]])
    return stations_data