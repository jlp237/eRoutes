# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

###1

import json
import requests
import pandas as pd

encoded_body = json.dumps({"station-get-surface": {"min-lat": 0,"max-lat": 45,"min-long": 30,
                                                   "max-long": 40}})

request = requests.post('https://api.plugsurfing.com/api/v4/request',
                 headers={'Content-Type': 'application/json',
                       'Authorization': 'key=a39ff3fb-fe0a-40a3-bdde-df6372c07c89'},
                 data=encoded_body)

dataJSON = request.json()
stationsJSON = dataJSON['stations']

stationID = stationsJSON[0]['id']
stationLon = stationsJSON[0]['longitude']
stationLat = stationsJSON[0]['latitude']


print(stationsJSON)

#
#print(json_data)
#
#df = pd.read_json(r.text, typ='series', lines=True, orient='records')
#
#print(df2)

 ###2
 
#import json
#import requests
#import pandas as pd
#
#encoded_body = json.dumps({"vehicle-get-all": {}})
#
#r = requests.post('https://api.plugsurfing.com/api/v4/request',
#                 headers={'Content-Type': 'application/json',
#                       'Authorization': 'key=a39ff3fb-fe0a-40a3-bdde-df6372c07c89'},
#                 data=encoded_body)
#
#df = pd.read_json(('[' + r.text.replace('}\n', '},') + ']'))
#
#
#print(df)
#
#
