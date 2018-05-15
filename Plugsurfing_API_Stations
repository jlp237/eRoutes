#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  8 20:18:06 2018

@author: vancura
"""

import json
import requests
import pandas as pd

## Step 1 - Get station IDs with geo data

# Create params variable with geodata of GER (for tests: smaller range)

encodedBodyStations = json.dumps({"station-get-surface": {"min-lat": 0,"max-lat": 45,"min-long": 30,
                                                   "max-long": 40}})

# Create JSON Request

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

stationPrices = pd.DataFrame(columns = ['Station_ID', 'Price'])

# determine quantity of groups

maxGroup = round(len(stations)/10)

# for-loop all groups and determine prices for each id in group

for i in range(maxGroup):
    print("Outer loop: " + str(i))
    for j in range(len(stations)):
        print("Inner loop: " + str(j) + " for group no " + str(groupCount))
        if(groupCount == stations['Group'][j]):
            tempStations.append(int(stations['Station_ID'][j]))
            
    encodedBodyStationPrices = json.dumps({"station-get-by-ids":{"station-ids":
        tempStations}})
    requestStationPrices = requests.post('https://api.plugsurfing.com/api/v4/request',
                            headers={'Content-Type': 'application/json',
                                     'Authorization': 'key=a39ff3fb-fe0a-40a3-bdde-df6372c07c89'},
                                     data=encodedBodyStationPrices)
    stationDataPricesJSON = requestStationPrices.json()
    stationPricesJSON = stationDataPricesJSON['stations']
    
    # insert length of current group instead of 6
    
    for k in range(6):
        stationPrices.loc[k] = [stationPricesJSON[k]['id'], stationPricesJSON[k]['connectors']]
#        stationPrices.append([stationPricesJSON[k]['id'], stationPricesJSON[k]['connectors']])
        
    tempStations = list()
    groupCount = groupCount + 1


            
# get station data and store it in dataframe
    
#for i in range(len(stations)):
#    if(groupCount == stations['Group'][i]):
#            tempStations.append(int(stations['Station_ID'][i]))
#            
    
    

        
#        encodedBodyStations = json.dumps({"station-get-by-ids":{"station-ids":
#        tempStations['Station_ID']}})
    

# Create params variable with geodata of GER (for tests: smaller range)

#encodedBodyStations = json.dumps({"station-get-surface": {"min-lat": 0,"max-lat": 45,"min-long": 30,
#                                                   "max-long": 40}})

# Create JSON Request

#requestStations = requests.post('https://api.plugsurfing.com/api/v4/request',
#                 headers={'Content-Type': 'application/json',
#                       'Authorization': 'key=a39ff3fb-fe0a-40a3-bdde-df6372c07c89'},
#                 data=encodedBodyStations)