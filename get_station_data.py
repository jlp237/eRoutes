#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  8 20:18:06 2018
@author: vancura
"""

import mysql.connector   

def get_connection () :
    
    connection = mysql.connector.connect(user='USER', password='PASSWORD',
                                         host='mobility.f4.htw-berlin.de',
                                         database='stations', buffered=True)
    return connection
    


def get_station_price (lat, long):
    
    connection = get_connection()
    
    # searching stations in radius 0.001 around long and lat
    # first check via sql query: count number of results 
    
    try:
        cursor = connection.cursor()
        selectString = ("select count(charging_per_kwh) from plugsurfing where "
                                            "latitude > %s and latitude < %s "
                                            "and longitude > %s and longitude < %s "
                                            "and charging_per_kwh > 0.00")
        data = (lat - 0.0005, lat + 0.0005, long - 0.0005, long +0.0005)
        cursor.execute(selectString, data)
        results = cursor.fetchone()
        
        # if there are results, return the exact price
        
        if(results[0] > 0):
             
            cursor2 = connection.cursor()
            selectString2 = ("select name, charging_per_kwh, type from plugsurfing where "
                                                "latitude > %s and latitude < %s "
                                                "and longitude > %s and longitude < %s "
                                                "and charging_per_kwh > 0.00")
            data2 = (lat - 0.0005, lat + 0.0005, long - 0.0005, long +0.0005)
            cursor2.execute(selectString2, data2)
            tmpResult2 = cursor2.fetchone()
            result2 = [tmpResult2[0], round(float(tmpResult2[1]),2), tmpResult2[2]]
            return result2;
            
        # if there are no results, check the stations close to the 
        # requested stations and return the average price
        
        else:
            cursor3 = connection.cursor()
            selectString3 = ("select name, avg(charging_per_kwh) from plugsurfing where "
                                            "latitude > %s and latitude < %s "
                                            "and longitude > %s and longitude < %s "
                                            "and charging_per_kwh > 0")
            data3 = (lat - 0.5, lat + 0.5, long - 0.5, long +0.5)
            cursor3.execute(selectString3, data3)
            tmpResult3 = cursor3.fetchone()
            result3 = [tmpResult3[0], round(tmpResult3[1],2), '-']
            return result3;

    finally:
        connection.close()



def get_station_charging_speed (lat, long):
    
    connection = get_connection()
        
    try:
        cursor = connection.cursor()
        selectString = ("select charging_speed from plugsurfing where "
                                            "latitude > %s and latitude < %s "
                                            "and longitude > %s and longitude < %s "
                                            "and charging_speed <> '0kW'")
        data = (lat - 0.0005, lat + 0.0005, long - 0.0005, long +0.0005)
        cursor.execute(selectString, data)
        result = cursor.fetchone()
        return result
    finally:
        connection.close()
       


def get_station_data (geodata):
    
    station_list = []
    stations_data = []
    
    for i in geodata:
        station_list.append(i.split(','))
    
    # search and return prices and charging_speed
    for i, j in station_list:
        station_data = get_station_price(float(i), float(j))
        stations_data.append([station_data[0], station_data[1]])    
    return stations_data

results = get_station_data(my_data_request)
