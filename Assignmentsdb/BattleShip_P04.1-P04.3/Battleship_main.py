#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 21:57:51 2022

@author: shyam
"""
 
#!/usr/bin/python
import psycopg2
import sys
import pprint
import random
from geojson import Polygon, Point, MultiPoint
import json
cardinalList = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
degree_middle = [0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5, 180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5]
from_degrees=[348.75, 11.25, 33.75, 56.25, 78.75, 101.25, 123.75, 146.25, 168.75, 191.25, 213.75, 236.25, 258.75, 281.25, 303.75, 326.25]
to_degrees=[11.25, 33.75, 56.25, 78.75, 101.25, 123.75, 146.25, 168.75, 191.25, 213.75, 236.25, 258.75, 281.25, 303.75, 326.25, 348.75]
rand_degrees = random.uniform(0, 360)
degrees = int(float(rand_degrees))
index = int((degrees + 11.25) / 22.5)
direction_move = cardinalList[index % 16]

boundary_away = cardinalList[(index + 8) % 16]
Ship_angle = cardinalList[(index + 8) % 16]


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



boundingbox = {
    "UpperLeft": {"lon": -10.31324002, "lat": 50.17116998},
    "LowerRight": {"lon": -8.06068579, "lat": 48.74631646},
}



class MyDatabase(object):
    def __enter__(self):
        with open("/Users/shyam/Downloads/config.json") as f:
            self.pgadminaccess = json.load(f)
        self.conn = psycopg2.connect(
            "dbname='"
            + self.pgadminaccess["dbname"]
            + "' "
            + "user='"
            + self.pgadminaccess["user"]
            + "' "
            + "host='"
            + self.pgadminaccess["host"]
            + "' "
            + "password='"
            + self.pgadminaccess["password"]
            + "' "
            + "port="
            + self.pgadminaccess["port"]
            + " "
        )
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()
        

conn = psycopg2.connect(database="BattleShip", user='postgres', password='Gangster30', host='localhost', port= '5432')

cursor = conn.cursor()

cursor.execute('''INSERT INTO Ship(, LAST_NAME, AGE, SEX, INCOME) 
   VALUES ('Ramya', 'Rama priya', 27, 'F', 9000)''')
cursor.execute('''INSERT INTO EMPLOYEE(FIRST_NAME, LAST_NAME, AGE, SEX, INCOME) 
   VALUES ('Vinay', 'Battacharya', 20, 'M', 6000)''')
cursor.execute('''INSERT INTO EMPLOYEE(FIRST_NAME, LAST_NAME, AGE, SEX, INCOME) 
   VALUES ('Sharukh', 'Sheik', 25, 'M', 8300)''')
cursor.execute('''INSERT INTO EMPLOYEE(FIRST_NAME, LAST_NAME, AGE, SEX, INCOME) 
   VALUES ('Sarmista', 'Sharma', 26, 'F', 10000)''')
cursor.execute('''INSERT INTO EMPLOYEE(FIRST_NAME, LAST_NAME, AGE, SEX, INCOME) 
   VALUES ('Tripthi', 'Mishra', 24, 'F', 6000)''')

# Commit your changes in the database
conn.commit()

conn.close()

box = f"""SELECT ST_AsGeoJson(ST_MakeEnvelope({boundingbox['UpperLeft']['lon']}, {boundingbox['UpperLeft']['lat']},
                     {boundingbox['LowerRight']['lon']}, {boundingbox["LowerRight"]['lat']}
                     ));"""   
    
with MyDatabase() as cur:
    cur.execute(box)
    bbox=cur.fetchall()[0][0]
    box=Polygon(json.loads(bbox)["coordinates"][0])



random_pos=(random.choice(cardinalList))
with MyDatabase() as cur:
    c_degrees = f"""SELECT start_degree, middle_degree, end_degree FROM cardinalDegrees WHERE direction = '{random_pos}'"""
    cur.execute(c_degrees)

import json
import psycopg2

with psycopg2.connect(database="BattleShip", user='postgres', password='Gangster30', host='localhost', port= '5432') as conn:
    with conn.cursor() as cur:
        with open('/Users/shyam/Downloads/Ships.json') as my_file:
            data = json.load(my_file)
            cur.execute(""" create table if not exists Ships_data(
                id integer, category text, shipClass text, length integer,width integer,armament json, armor json, speed integer, turn_radius integer,
                location integer) """)
            query_sql = """ insert into Ships_data
                select * from json_populate_recordset(NULL::Ships_data, %s) """
            cur.execute(query_sql, (json.dumps(data),))


centroid="SELECT ST_AsGeoJson(ST_Centroid(ST_GeomFromGeoJSON('" + str(bbox) + "')))"
with MyDatabase() as cur:
    cur.execute(centroid)
    centroid_pt =Point(json.loads(cur.fetchall()[0][0])["coordinates"])


least_deg = from_degrees[index % 16]
max_deg = to_degrees[index % 16]


def sector_gen(centroid_pt,least_deg,max_deg,bbox):
    rand_degrees = random.uniform(0, 360)
    degrees = int(float(rand_degrees))
    index = int((degrees + 11.25) / 22.5)
    direction_move = cardinalList[index % 16]
    index = int((rand_degrees + 11.25) / 22.5)
    direction = cardinalList[index % 16]
    highest_deg = from_degrees[index % 16]
    Lowest_deg = to_degrees[index % 16]
    sector_line1 = "SELECT ST_AsGeoJSON(ST_Intersection(ST_Project(ST_GeomFromGeoJSON('" + str(centroid_pt) + "'), 80000, radians(" + str(least_deg) + ")), ST_GeomFromGeoJSON('" + str(bbox) + "')))"
    sector_line2 = "SELECT ST_AsGeoJSON(ST_Intersection(ST_Project(ST_GeomFromGeoJSON('" + str(centroid_pt) + "'), 80000, radians(" + str(max_deg) + ")), ST_GeomFromGeoJSON('" + str(bbox) + "')))"    
    with MyDatabase() as conn:
        with conn.cursor() as curs:
            curs.execute(sector_line1)
            sector_point1 = Point(json.loads(cur.fetchall()[0][0])["coordinates"])
            curs.execute(sector_line2)
            sector_line2 = Point(json.loads(cur.fetchall()[0][0])["coordinates"])
            get_sector = "SELECT ST_AsGeoJSON(ST_MakePolygon(ST_MakeLine((ARRAY[ST_GeomFromGeoJSON('" + str(centroid_pt) + "'), ST_GeomFromGeoJSON('" + str(sector_point1) + "'), ST_GeomFromGeoJSON('" + str(sector_line2) + "'), ST_GeomFromGeoJSON('" + str(centroid_pt) + "')]))))"
            curs.execute(get_sector)
            conn.close()
            region = Polygon(json.loads(cur.fetchall()[0][0])["coordinates"])
    return(region)


def Place_ships(region):
    with MyDatabase() as conn:
        with conn.cursor() as curs:
            center_pt_ships="select ST_AsGeoJSON(ST_Centroid(ST_GeomFromGeoJSON('" + str(region) + "')))"
            curs.execute(center_pt_ships)
            Center_boat = Point(json.loads(curs.fetchall()[0][0])["coordinates"])
            random_ship= "UPDATE ships SET location = ST_GeomFromGeoJSON(%s), bearing = " + str(Ship_angle) + " WHERE id = %s"
            Spacing = "SELECT ST_AsGeoJSON(ST_Project(ST_Project(ST_GeomFromGeoJSON('" + str(Center_boat) + "'), 111, radians(270)), 111, radians(0)))"
            Space1 = Center_boat
            Space2 = "SELECT ST_AsGeoJSON(ST_Project(ST_GeomFromGeoJSON('" + str(Center_boat) + "'), 111, radians(180)))"
            curs.execute(Spacing)
            Spacing=Point(json.loads(curs.fetchall()[0][0])["coordinates"])
            curs.execute(Space2)
            Space2 = Point(json.loads(curs.fetchall()[0][0])["coordinates"])
            Space3 = "SELECT ST_AsGeoJSON(ST_Project(ST_Project(ST_GeomFromGeoJSON('" + str(Space2) + "'), 111, radians(270)), 111, radians(180)))"
            curs.execute(Space3)
            Space3 = Point(json.loads(curs.fetchall()[0][0])["coordinates"])
            curs.execute(random_ship, (json.dumps(Spacing),3))
            curs.execute(random_ship, (json.dumps(Space1), 0))
            curs.execute(random_ship, (json.dumps(Space2), 1))
            curs.execute(random_ship, (json.dumps(Space3), 2))
            curs.execute(random_ship)
            for i in range(0, 4):
                if i == 4:
                    point_sec = "SELECT ST_AsGeoJSON(ST_Project(ST_GeomFromGeoJSON(%s), 111, radians(270)))"
                    Space1 = Point(json.loads(curs.fetchall()[0][0])["coordinates"])
                    Space1 = Point(json.loads(curs.fetchall()[0][0])["coordinates"])
                    curs.execute(point_sec, (json.dumps(Space1), i))
                elif i== 1:
                         point_sec = "SELECT ST_AsGeoJSON(ST_Project(ST_GeomFromGeoJSON('" + str(Space2) + "'), 222, radians(270)))"
                         curs.execute(point_sec)
                         Space2 = Point(json.loads(curs.fetchall()[0][0])["coordinates"])
                         curs.execute(point_sec, (json.dumps(Space2), i))
                elif i == 2:
                        point_sec = "SELECT ST_AsGeoJSON(ST_Project(ST_GeomFromGeoJSON('" + str(Space3) + "'), 222, radians(270)))"
                        curs.execute(point_sec)
                        Space3 = Point(json.loads(curs.fetchall()[0][0])["coordinates"])
                        curs.execute(point_sec, (json.dumps(Space3), i))
                else:
                        point_sec = "SELECT ST_AsGeoJSON(ST_Project(ST_GeomFromGeoJSON('" + str(Spacing) + "'), 222, radians(270)))"
                        curs.execute(point_sec)
                        Spacing= Point(json.loads(curs.fetchall()[0][0])["coordinates"])
                        curs.execute(point_sec, (json.dumps(Spacing), i))
        fleet_response = {
                    "fleet_id": random.randint(1,30),
                    "ship_status": []
                }
        
        response = "SELECT id, bearing, ST_asGeoJSON(location) FROM ships ORDER BY id ASC"
        with MyDatabase() as cur:
            cur.execute(response)
            response = cur.fetchall()
        for result in response:
            fleet_response["ship_status"].append({"ship_id": result[0], "bearing": result[1], "location": {"lon": json.loads(result[2])["coordinates"][0], "lat":json.loads(result[2])["coordinates"][1]}})
        with open("/Users/Shyam/Downloads/Battle_Ship.json", "w") as out:
            json.dump(fleet_response, out, indent=4)
    return("done")    
                




