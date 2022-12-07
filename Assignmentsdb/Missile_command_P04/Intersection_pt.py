#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 18:02:04 2022

@author: shyam
"""


##### request URL

import requests
import json
import numpy as np
import random
from shapely.geometry import Polygon, Point
import typing
import psycopg2
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import json
from cmath import pi
from math import radians, cos, sin, sqrt, degrees, asin, atan2, acos
import numpy
import math
import time
from math import sin, cos, sqrt, atan2
import geopy.distance



def Request_team_id():
    get_teamID_url= f"http://missilecommand.live:8080/START/2"
    teamID = requests.get(get_teamID_url)
    if teamID.status_code == 200:
        teamID_info=(json.loads(teamID.content.decode('utf-8')))
    return(teamID_info)

def Request_radar():
    get_radarsweep=f"http://missilecommand.live:8080/RADAR_SWEEP"
    radar = requests.get(get_radarsweep)
    if radar.status_code == 200:
        radar_info=(json.loads(radar.content.decode('utf-8')))
    return(radar_info)


def Request_registeruser():
    get_radarsweep=f"http://missilecommand.live:8080/REGISTER"
    register = requests.get(get_radarsweep)
    if register.status_code == 200:
        register_info=(json.loads(register.content.decode('utf-8')))
    else:
        register_info='No data found'
    return(register_info)

def Request_time():
    get_clock=f"http://missilecommand.live:8080/GET_CLOCK"
    current_time = requests.get(get_clock)
    if current_time.status_code == 200:
        current_time=(json.loads(current_time.content.decode('utf-8')))
    return(current_time)


def dict_get(x,key,here=None):
    x = x.copy()
    if here is None: here = []
    if x.get(key):  
        here.append(x.get(key))
        x.pop(key)
    else:
        for i,j in x.items():
          if  isinstance(x[i],list): dict_get(x[i][0],key,here)
          if  isinstance(x[i],dict): dict_get(x[i],key,here)
    return here




def parse_radar():
    radar_response=Request_radar()
    coordinates=[]
    bearings=[]
    altitudes=[]
    missile=[]
    radar_response=dict_get(radar_response,'features')[0]
    for i in range(0,len(radar_response)):
        print(i)
        coord=dict_get(radar_response[i],'geometry')[0]['coordinates']
#        coord[0]=radians(float(coord[0]))
#        coord[1]=radians(float(coord[1]))
        bearing=dict_get(radar_response[i],'properties')[0]['bearing']
        altitude=dict_get(radar_response[i],'properties')[0]['altitude']
        missile_type=dict_get(radar_response[i],'properties')[0]['missile_type']
        coordinates.append(coord)
        bearings.append(bearing)
        altitudes.append(altitude)
        missile.append(missile_type)
    lis=[coordinates,bearings,altitudes,missile]
    return(lis)    



radar_info=parse_radar()
def get_batteries_positions(radar_info):
    missile_positions=[]
    Region_response=Request_registeruser()
    Multipolygon_regions=dict_get(Region_response,'region')[0]
    poly_set=Multipolygon_regions['features'][0]['geometry']['coordinates']
    len_incomingmissiles=len(radar_info[0])
    missile_pos=random.sample(poly_set,len_incomingmissiles)
    for i in range(0,len(missile_pos)):
        positions=random.sample(missile_pos[i][0], 1)[0]
        missile_positions.append(positions)
    return(missile_positions)        

def get_bearing(lat1, long1, lat2, long2):
    dLon = (long2 - long1)
    x = math.cos(math.radians(lat2)) * math.sin(math.radians(dLon))
    y = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(dLon))
    brng = numpy.arctan2(x,y)
    brng = numpy.degrees(brng)
    return brng


from geopy import distance
def get_distance(missile_positions,radar_info):
    distances=[]
    intersections=[]
    missiles['coordinates']=pd.Series(missile_positions[:11])
    for j in range(0,len(radar_info[0])):
            coords_1 = (missile_positions[j][1], missile_positions[j][0])
            coords_2 = (radar_info[0][j][1], radar_info[0][j][0])
            dist=(distance.distance(coords_1, coords_2).miles)
            distances.append(dist)
            start_bearing=get_bearing(list(coords_1)[1],list(coords_1)[0], list(coords_2)[1],list(coords_2)[0])
            inetrs=intersection_pt(list(coords_1)[0],list(coords_1)[1],start_bearing,list(coords_2)[0],list(coords_2)[1],radar_info[1][i])
            intersections.append(inetrs)
     missiles["distance"]=pd.Series(distances)
     missiles['fire_time']=missiles["distance"]/missiles["mph"]
     missiles['target_lat/lon']  =pd.Series(intersections)
    return(distances,intersections)





connection = psycopg2.connect(user="postgres",
                                  password="Gangster30",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="Datamodel")
import psycopg2

import pandas as pds

from sqlalchemy import create_engine

 

# Create an engine instance
conn_string = "host='localhost' dbname='Datamodel' user='postgres' password='Gangster30'"
conn = psycopg2.connect(conn_string)
missile_speed  = pds.read_sql("select * from missile_speed", conn)
missile_blast  = pds.read_sql("select * from missile_blast", conn)
missile  = pds.read_sql("select * from missile", conn)
missile_properties=pd.concat([missile_blast,missile_speed],axis=1)
missile_properties = missile_properties.loc[:,~missile_properties.columns.duplicated()].copy()
missiles = pd.merge(missile_properties,missile, how='left',left_on=['category'],right_on=['speedCat']).dropna().reset_index()
missiles.drop(['index', 'category_x'],axis=1,inplace=True)
missiles.columns=['blast_radius', 'ms', 'mph', 'category', 'name', 'speedCat','blastCat']

# Connect to PostgreSQL server



sql = """
    WITH 
        Q1 AS (
            SELECT ST_SetSRID(ST_Project('POINT({45.850186} {-84.603171})'::geometry, 2340, -115.27)::geometry,4326) as p2
        )"""

results = cursor.execute(sql)
 


def assign_antimissile(current_radar,missiles_place):
    anti_missiles=get_batteries_positions()
    missiles['coordinates']=pd.Series(anti_missiles)
    for times in range(5):
        start = time.time()
        time.sleep(times)
        current_radar=parse_radar()
    
                
import shapely
from shapely.geometry import LineString, Point

line1 = LineString(list(coords_1))
line2 = LineString(list(coords_2))

int_pt = line1.intersection(line2)
point_of_intersection = int_pt.x, int_pt.y

print(point_of_intersection)


def intersection_pt(x1,y1,b1,x2,y2,b2):
      lon1 = radians(float(x1))
      lat1 = radians(float(y1))
      b1 = radians(float(b1))

      lon2 = radians(float(x2))
      lat2 = radians(float(y2))
      b2 = radians(float(b2))

      dlon = lon2 - lon1 # Distance between longitude points
      dlat = lat2 - lat1 # Distance between latitude points
      haversine = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
      ang_dist_1_2 = 2 * asin(sqrt(haversine))
      initial_bearing = acos((sin(lat2) - sin(lat1) * cos(ang_dist_1_2)) / (sin(ang_dist_1_2) * cos(lat1)))
      final_bearing = acos((sin(lat1) - sin(lat2) * cos(ang_dist_1_2)) / (sin(ang_dist_1_2) * cos(lat2)))
      if sin(x2 - x1) > 0:
          bearing_1_2 = initial_bearing
          bearing_2_1 = (2 * pi) - final_bearing
      else:
          bearing_1_2 = (2 * pi) - initial_bearing
          bearing_2_1 = final_bearing
      ang_1 = b1 - bearing_1_2    # angle p2<--p1-->p3
      ang_2 = bearing_2_1 - b2    # angle p1<--p2-->p3
      ang_3 = acos(-cos(ang_1) * cos(ang_2) + sin(ang_1) * sin(ang_2) * cos(ang_dist_1_2))    # angle p1<--p3-->p2
      ang_dist_1_3 = atan2(sin(ang_dist_1_2) * sin(ang_1) * sin(ang_2), cos(ang_2) + cos(ang_1) * cos(ang_3))
      lat3 = asin(sin(lat1) * cos(ang_dist_1_3) + cos(lat1) * sin(ang_dist_1_3) * cos(b1))
      delta_long_1_3 = atan2(sin(b1) * sin(ang_dist_1_3) * cos(lat1), cos(ang_dist_1_3) - sin(lat1) * sin(lat3))
      lon3 = lon1 + delta_long_1_3
      print("Lat3 : ", lat3)
      print("Lon3 : ", lon3)
      return(lat3,lon3)  

geolocator = Nominatim(user_agent="geoapiExercises")

print(geolocator.reverse([30.309562912874206,-118.19674690386668]))

intersection_pt(-80.299741,25.405385,-72.5537221634294,-123.271325049, 30.313422612,0.9905586)    


(-0.13301775519129927, -79.27464448755403)




#get_bearing( -80.299741,25.405385, -123.271325049, 30.313422612)





import psycopg2 
import json 
conn=psycopg2.connect("dbname='Missile_command' user='postgres' host= localhost password='Gangster30'") 
cur = conn.cursor() 
ur_dict =Request_registeruser()
cur.execute('''SELECT ST_3DDistance(
			ST_Transform('SRID=4326;POINT(-72.1235 42.3521 1)'::geometry,2163),
			ST_Transform('SRID=4326;POINT(-72.1235 42.3521 20000)'::geometry,2163)
		) As dist_3d''')
        

    






# SELECT ST_3DDistance(
# 			ST_Transform('SRID=4326;POINT(-72.1235 42.3521 1)'::geometry,2163),
# 			ST_Transform('SRID=4326;POINT(-72.1235 42.3521 20000)'::geometry,2163)
# 		) As dist_3d



#SELECT ST_AsText(ST_Project('POINT(-98 34)'::geography, 555, radians(45.0)));



# WITH 
# Q1 AS (
#     SELECT 'POINT(-98 34)'::geometry as p1
# ), 

# Q2 AS (
#      SELECT ST_Project('POINT(-98 34)'::geometry, 555, radians(45.0))::geometry as p2
# )

# SELECT ST_MakeLine(ST_Point(ST_X(p1),ST_Y(p1)), ST_Point(ST_X(p2),ST_Y(p2))) as missilePath

# FROM Q1, Q2;



#     WITH 
#         Q1 AS (
#             SELECT ST_SetSRID(ST_Project('POINT(-98 34)'::geometry, 66600, radians(270))::geometry,4326) as p2
#         )
 
# SELECT jsonb_build_object(
#     'type',       'Feature',
#     'geometry',   ST_AsGeoJSON(p2)::jsonb,
# 	'properties', null
#     ) AS json
# FROM Q1



############# Intersection point



######### Calculate radius
def calculate_radius():
    x1, y1 = input("Enter the coordinates of the center of the circle (x, y): ").split(',')
    x2, y2 = input("Enter the coordinates of the point on the circle (x, y): ").split(',')
        
    x1,y1 = int(x1), int(y1)
    x2,y2 = int(x2), int(y2)

    radius = Circle.point_distance(x1, y1, x2, y2)
    area = Circle.area_calc(radius)
    perimeter = Circle.perimeter_calc(radius)
    print("Radius :", radius)
    
######### Time calculation

def time_counter(seconds):
    starttime = time.time()
    while True:
        now = time.time()
        if now > starttime + seconds:
            break
        yield now - starttime



##########Calculate intercept

def get_intercept(start_coords,radar_sweep=0):
    for t in time_counter(20):
        radar_sweep=t
        time.sleep(3)
    x1 = start_coords[0]
    y1 = start_coords[1]
    b1 = 0
    x2 = radar_sweep[0]
    y2 = radar_sweep[1]
    b2 = 100
    
    
def show_warning(title, message):
    return messagebox.showwarning(title, message)




######### extract vertices from Geojson file






    
    









