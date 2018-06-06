import json
import requests
import pandas as pd
import math
import mysql.connector


def getStationData(min_lat, max_lat, min_long, max_long):
    ## Step 1 - Get station IDs with geo data

    # Create params variable with geodata of GER (for tests: smaller range)

    encodedBodyStations = json.dumps(
        {"station-get-surface": {"min-lat": min_lat, "max-lat": max_lat, "min-long": min_long,
                                 "max-long": max_long}})

    # API-request #2: stations in geodata

    requestStations = requests.post('https://api.plugsurfing.com/api/v4/request',
                                    headers={'Content-Type': 'application/json',
                                             'Authorization': 'key=API-KEY'},
                                    data=encodedBodyStations)

    # reduce JSON string to station data as list

    StationsDataJSON = requestStations.json()
    stationsJSON = StationsDataJSON['stations']
    stations = pd.DataFrame(columns=['Group', 'Station_ID', 'Latitude', 'Longitude'])

    groupCount = 0

    # max number of IDs per call is ten. Thus, IDs are splitted into groups of ten.

    for i in range(len(stationsJSON)):
        if (i % 10 == 0):
            groupCount = groupCount + 1
            stations.loc[i] = [groupCount, stationsJSON[i]['id'],
                               stationsJSON[i]['latitude'],
                               stationsJSON[i]['longitude']]
        else:
            stations.loc[i] = [groupCount, stationsJSON[i]['id'],
                               stationsJSON[i]['latitude'],
                               stationsJSON[i]['longitude']]

    # info msg

    print("Preload of " + str(len(stations)) + " stations.")

    ## Step 2 - Get prices of stations

    # maximum of 10 station ids per call based on "Group"-column

    groupCount = 1
    tempStations = list()

    stationPrices = pd.DataFrame(
        columns=['Station_ID', 'Name', 'Latitude', 'Longitude', 'Type', 'Charging_Speed', 'Charging_per_kwh'])

    # determine quantity of groups

    maxGroup = math.ceil((len(stations) / 10))

    # setting idPointer to 1 to determine each group length in for-loop 3

    idPointer = 1;

    # for-loop 1: for-loop through all existing groups
    for i in range(maxGroup):
        # for-loop 2: for-loop through all existing stations in geodata (see above)
        for j in range(len(stations)):
            if (groupCount == stations['Group'][j]):
                tempStations.append(int(stations['Station_ID'][j]))

                # API-request #2: station data

        encodedBodyStationPrices = json.dumps({"station-get-by-ids": {"station-ids":
                                                                          tempStations}})
        requestStationPrices = requests.post('https://api.plugsurfing.com/api/v4/request',
                                             headers={'Content-Type': 'application/json',
                                                      'Authorization': 'key=API-KEY'},
                                             data=encodedBodyStationPrices)
        stationDataPricesJSON = requestStationPrices.json()
        stationPricesJSON = stationDataPricesJSON['stations']

        # for-loop 3: insert length of current group as length of tempStations
        # prices type = dict if charging-per-kwh is available

        for k in range(len(tempStations)):
            if (isinstance(stationPricesJSON[k]['connectors'][0]['prices'], dict)):
                stationPrices.loc[idPointer] = [stationPricesJSON[k]['id'],
                                                stationPricesJSON[k]['name'],
                                                stationPricesJSON[k]['latitude'],
                                                stationPricesJSON[k]['longitude'],
                                                stationPricesJSON[k]['connectors'][0]['name'],
                                                stationPricesJSON[k]['connectors'][0]['speed'],
                                                stationPricesJSON[k]['connectors'][0]['prices']['charging-per-kwh']]
            else:
                stationPrices.loc[idPointer] = [stationPricesJSON[k]['id'],
                                                stationPricesJSON[k]['name'],
                                                stationPricesJSON[k]['latitude'],
                                                stationPricesJSON[k]['longitude'],
                                                stationPricesJSON[k]['connectors'][0]['name'],
                                                stationPricesJSON[k]['connectors'][0]['speed'],
                                                "N/A"]
            idPointer = idPointer + 1;
            print(str(round(idPointer / len(stations) * 100, 2)) + "% of stations loaded.")

        tempStations = list()
        groupCount = groupCount + 1

        ## Step 3 - Store all information in MySQL database "stations" in table "plugsurfing"

    # connection to HTW Mobility MySQL - DB and preset stations as database

    print("Connecting to MySQL Server.")

    connection = mysql.connector.connect(user='dsteiner', password='eMobility2018DS',
                                         host='mobility.f4.htw-berlin.de',
                                         database='stations')

    # try / finally for potential erros in SQL queries

    try:
        cursor = connection.cursor()
        for i, r in stationPrices.iterrows():
            insertString = ("insert into plugsurfing (station_id, name, latitude, longitude,"
                            " type, charging_speed,"
                            " charging_per_kwh) values "
                            "(%s, %s, %s, %s, %s, %s, %s)")
            data = (r['Station_ID'], r['Name'], r['Latitude'], r['Longitude'], r['Type'],
                    r['Charging_Speed'], r['Charging_per_kwh'])
            cursor.execute(insertString, data)
            print("Inserting station id " + str(stationPrices['Station_ID'][i]))
    finally:
        connection.commit()
        connection.close()
        print("Inserted " + str(len(stations)) + " stations in database.")


# get geodata of Germany from spreadsheet

# first part - 4955 stations (loaded)
# getStationData(47.27011,55.0815,5.866342,8.160230)

# second part - 2983 stations (loaded)
# getStationData(47.27011,55.0815,8.160230,10.45411)

# third part - 1423 stations (loaded)
# getStationData(47.27011,55.0815,10.45411,12.74800)

# fourth part - 1409 stations (loaded)
# getStationData(47.27011,55.0815,12.74800,15.04189)


# get prices from specific station

geodata_JLP_found = pd.DataFrame(columns=['Name', 'Latitude', 'DifLat', 'Longitude', 'DifLong', 'Charging_per_kwh'])


def getStationPrices(lat, long):
    connection = mysql.connector.connect(user='dsteiner', password='eMobility2018DS',
                                         host='mobility.f4.htw-berlin.de',
                                         database='stations')

    try:
        cursor = connection.cursor()
        selectString = ("select name, latitude, longitude, charging_per_kwh from plugsurfing where "
                        "latitude > %s and latitude < %s "
                        "and longitude > %s and longitude < %s")
        data = (lat - 0.0005, lat + 0.0005, long - 0.0005, long + 0.0005)
        cursor.execute(selectString, data)
    finally:
        connection.close()

    for (name, latitude, longitude, charging_per_kwh) in cursor:
        if (latitude is not None):
            return ([name, latitude, latitude - lat, longitude, longitude - long,
                     charging_per_kwh])
        else:
            break;


counter = 0


# function for providing price of specific station

def getStationPrice(lat, long):
    connection = mysql.connector.connect(user='tvancura', password='eMobility2018TV',
                                         host='mobility.f4.htw-berlin.de',
                                         database='stations')

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

        for cpk in cursor:
            results = cpk

        # if there are results, return the exact price

        if (results[0] > 0):

            cursor2 = connection.cursor()
            selectString2 = ("select charging_per_kwh from plugsurfing where "
                             "latitude > %s and latitude < %s "
                             "and longitude > %s and longitude < %s "
                             "and charging_per_kwh > 0.00")
            data2 = (lat - 0.0005, lat + 0.0005, long - 0.0005, long + 0.0005)
            cursor2.execute(selectString2, data2)
            for row2 in cursor2:
                result2 = float(row2[0])
                return result2;

        # if there are no results, check the stations close to the requested stations and return the average price

        else:
            cursor3 = connection.cursor()
            selectString3 = ("select avg(charging_per_kwh) from plugsurfing where "
                             "latitude > %s and latitude < %s "
                             "and longitude > %s and longitude < %s "
                             "and charging_per_kwh > 0")
            data3 = (lat - 0.5, lat + 0.5, long - 0.5, long + 0.5)
            cursor3.execute(selectString3, data3)
            for row3 in cursor3:
                result3 = float(round(row3[0], 2))
                return result3

    finally:
        connection.close()

# prerequisit -> geodata_JLP imported as Array
# for i, j in geodata_JLP:
#    print("Wert " + str(i) + " und " + str(j))
#    print(getStationPrice(float(i),float(j)))
