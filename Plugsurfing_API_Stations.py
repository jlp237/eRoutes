#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  8 20:18:06 2018

@author: vancura
"""

import json
import requests
import pandas as pd
import math
import mysql.connector   

## Step 1 - Get station IDs with geo data

# Create params variable with geodata of GER (for tests: smaller range)

encodedBodyStations = json.dumps({"station-get-surface": {"min-lat": 0,"max-lat": 145,"min-long": 30,
                                                   "max-long": 40}})

# API-request #2: stations in geodata

requestStations = requests.post('https://api.plugsurfing.com/api/v4/request',
                 headers={'Content-Type': 'application/json',
                       'Authorization': 'key=a39ff3fb-fe0a-40a3-bdde-df6372c07c89'},
                 data=encodedBodyStations)

# reduce JSON string to station data as list

StationsDataJSON = requestStations.json()
stationsJSON = StationsDataJSON['stations']
stations = pd.DataFrame(columns = ['Group', 'Station_ID', 'Latitude', 'Longitude'])

groupCount = 0

# max number of IDs per call is ten. Thus, IDs are splitted into groups of ten.


for i in range(len(stationsJSON)):
    if(i%10 == 0):
        groupCount = groupCount + 1
        stations.loc[i] = [groupCount, stationsJSON[i]['id'], 
                           stationsJSON[i]['latitude'], 
                           stationsJSON[i]['longitude']]
    else:
        stations.loc[i] = [groupCount, stationsJSON[i]['id'],
                           stationsJSON[i]['latitude'],
                           stationsJSON[i]['longitude']]


## Step 2 - Get prices of stations
    
# maximum of 10 station ids per call based on "Group"-column

groupCount = 1
tempStations = list()

stationPrices = pd.DataFrame(columns = ['Station_ID', 'Type', 'Charging_Speed', 'Charging-per-kwh'])

# determine quantity of groups

maxGroup = math.ceil((len(stations)/10))

# setting idPointer to 1 to determine each group length in for-loop 3

idPointer = 1;

# for-loop 1: for-loop through all existing groups
for i in range(maxGroup):
    # for-loop 2: for-loop through all existing stations in geodata (see above)
    for j in range(len(stations)):
        if(groupCount == stations['Group'][j]):
            tempStations.append(int(stations['Station_ID'][j]))
            
            # API-request #2: station data
            
    encodedBodyStationPrices = json.dumps({"station-get-by-ids":{"station-ids":
        tempStations}})
    requestStationPrices = requests.post('https://api.plugsurfing.com/api/v4/request',
                            headers={'Content-Type': 'application/json',
                                     'Authorization': 'key=a39ff3fb-fe0a-40a3-bdde-df6372c07c89'},
                                     data=encodedBodyStationPrices)
    stationDataPricesJSON = requestStationPrices.json()
    stationPricesJSON = stationDataPricesJSON['stations']
    
    # for-loop 3: insert length of current group as length of tempStations
    
    for k in range(len(tempStations)):
        if(isinstance(stationPricesJSON[k]['connectors'][0]['prices'], dict)):
            stationPrices.loc[idPointer] = [stationPricesJSON[k]['id'], 
                              stationPricesJSON[k]['connectors'][0]['name'],
                              stationPricesJSON[k]['connectors'][0]['speed'],
                              stationPricesJSON[k]['connectors'][0]['prices']['charging-per-kwh']]
        else:
            stationPrices.loc[idPointer] = [stationPricesJSON[k]['id'],
                              stationPricesJSON[k]['connectors'][0]['name'],
                              stationPricesJSON[k]['connectors'][0]['speed'],
                              "N/A"]
        idPointer = idPointer + 1;
        
    tempStations = list()
    groupCount = groupCount + 1

