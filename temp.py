#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 23 10:54:30 2018

@author: jan-lukaspflaum
"""

# neuer ansatz: schleife bauen , die eine route berechnet bis zum ersten polyline punkt, checkt ob gefahrene distanz < range of car ist. 
#  gefahrene distanz darf nicht > range sein. dann nimmt die funktion sich die koordinate von wegpunkt 200 km. 
# loop durchläuft alle abstände zwischen koordinate und stationen along route. es wird station zurückgegeben mit kleinstem abstand zur station. 
#wenn größer als range , dann in stationsliste eintrag x-1 (= eine station davor) auswählen == erste ladestation


# for visualization: 
# https://developer.here.com/api-explorer/geovisualization/technology_markers/markers-csv-provider

# to do: 

#integrate security puffer 

#integrate in temperature
#integrate battery level at start

temparature = 20.0
battery_level_at_start = 0.8
security_puffer_in_km = 50 
