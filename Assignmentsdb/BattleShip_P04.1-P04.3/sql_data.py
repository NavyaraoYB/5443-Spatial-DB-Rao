#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 01:24:39 2022

@author: shyam
"""

import psycopg2
import json
import time

class MyDatabase():
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


with MyDatabase() as conn:
    with conn.cursor() as curs:
        turn_fleet = f"""SELECT ss.ship_id::int, mod((ss.bearing + 60)::int, 360), ST_AsText(
        ST_Rotate(ss.geom, RADIANS((60 + ss.bearing) * 1)
        ))
         FROM public.ship_state as ss LIMIT 5;"""
        curs.execute(turn_fleet)
        new_poly = curs.fetchall()
        for i in range(len(new_poly)):
            head = ['ship_id', 'bearing', 'geometry']
            new_poly[i] = dict(zip(head, new_poly[i]))
        with open('queries.json', 'w') as f:
            f.write('// Query 1 Result:\n')
            f.write(json.dumps(new_poly, indent=4))

        turn_ship = f"""SELECT ST_Rotate(ss.geom, RADIANS(40 + ss.bearing)) FROM public.ship_state as ss WHERE ship_id = 7;"""
        curs.execute(turn_ship)
        new_poly = curs.fetchall()[0][0]
        update = f"""UPDATE ship_state SET speed = 25, bearing = (bearing + 40)::int % 360,  geom = '{new_poly}' WHERE ship_id = 7;"""
        curs.execute(update)
        update = f"""SELECT ship_id::int, speed::int, bearing, ST_AsText(geom) FROM ship_state WHERE ship_id = 7;"""
        curs.execute(update)
        update = curs.fetchall()[0]
        head = ["ship_id", 'new_speed', 'bearing', 'new_rotation']
        file = dict(zip(head, update))     
        with open('queries.json', 'a') as f:
            f.write("\n\n// Query 2 Result\n")
            f.write(json.dumps(file, indent=4))
        rotate_gun = f"""UPDATE gun_state
        SET bearing = (bearing + 10)::int % 360, elevation = (elevation + 5)::int % 45
        FROM ships_guns
        WHERE gun_state.ship_id = 2 and ships_guns.type = 'Mark13';"""
        curs.execute(rotate_gun)
        curs.execute("""SELECT gs.ship_id::int, gs.gun_id::int, type, bearing, elevation 
                     FROM gun_state as gs, ships_guns as sg 
                     WHERE gs.ship_id = sg.ship_id AND gs.gun_id = sg.gun_id
                     AND sg.type = 'Mark13' AND sg.ship_id = 2""")
        head = ['ship_id', 'gun_id', 'type', 'bearing', 'elevation']
        info = curs.fetchall()[0]
        file = dict(zip(head, info))
        with open('queries.json', 'a') as f:
            f.write("\n\n// Query 3 Result\n")
            f.write(json.dumps(file, indent=4))

        rof = f"""SELECT rof::int FROM ship_state as ss, gun_state as gs, projectile as prj, gun as g, ships_guns as shg
        WHERE ss.ship_id = 0 AND g.name = shg.type AND g.name = 'Mark8' AND shg.type = 'Mark8'
        AND prj.name = g.ammotype LIMIT 1;
        """
        curs.execute(rof)
        rof = curs.fetchall()[0][0]
        center_point = f"""ST_MakePoint((ss.location->>'lon')::float, (ss.location->>'lat')::float)"""
        projected_point = f"""ST_Project({center_point}, prj.mm::int * 10, RADIANS(gs.bearing))"""
        fire_gun = f"""SELECT ST_AsText(
        ST_MakeLine(
            ST_SetSRID({center_point}, 4326),
             ST_SetSRID({projected_point}::geometry, 4326)
            ))
            FROM ship_state as ss, gun_state as gs, projectile as prj, gun as g, ships_guns as shg
            WHERE ss.ship_id = 0 AND g.name = shg.type AND g.name = 'Mark8' AND shg.type = 'Mark8'
            AND prj.name = g.ammotype LIMIT {rof};"""
        curs.execute(fire_gun)
        path = curs.fetchall()[0][0]
        info = f"""SELECT ship_id::int, gun_id::int, type from ships_guns WHERE ship_id = 0 AND type = 'Mark8' LIMIT 1;"""
        curs.execute(info)
        head = ['ship_id', 'gun_id', 'type', 'path']
        info = list(curs.fetchall()[0])
        info.append(path)
        file = dict(zip(head, info))
       
        with open('queries.json', 'a') as f:
            f.write("\n\n// Query 4 Result\n")
            f.write(json.dumps(file, indent=4))
        update = f"""UPDATE gun_state SET ammo = ammo - {rof} from ships_guns
        WHERE ships_guns.gun_id = gun_state.gun_id AND ships_guns.type = 'Mark8' AND gun_state.ship_id = 0;"""
        curs.execute(update)
