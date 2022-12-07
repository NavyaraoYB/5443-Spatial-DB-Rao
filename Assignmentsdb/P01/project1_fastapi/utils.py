from dis import COMPILER_FLAG_NAMES
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, sessionmaker
import pandas as pd
from fastapi import Depends, FastAPI
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql import text
import sys



#my_database_connection="postgresql://user:Gangster30@server_ip/Project1"

alchemyEngine   = create_engine('postgresql://postgres:Gangster30@127.0.0.1/Project1', pool_recycle=3600);


# Connect to PostgreSQL server

dbConnection    = alchemyEngine.connect();

#conn = psycopg2.connect("dbname=Project1 user=postgres")
#cur = conn.cursor()
#engine=create_engine(my_database_connection)
#SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=alchemyEngine)
#Base=declarative_base()


def do_findall():
    df = pd.read_sql_query('select * from \"switzerland_new\"',con=alchemyEngine)
    return df

import sys
#sys.setrecursionlimit(50000)

def get_tuple(colname,value):
    df_getone = pd.read_sql_query('select * from \"switzerland_new\"',con=alchemyEngine)
    df_getone.columns=['name' ,'osm_type','class','type','lon','lat','place_rank', 'importance',	'street','city' ,	'county' , 'state','country', 'country_code', 'display_name','west' ,	'south'	,'east','north'	,'wikidata' ,'wikipedia','distance']
    return (df_getone[df_getone[colname].isin([value,'Switzerland'])]) 
    #dbConnection.execute("SELECT * FROM PacketManager WHERE {} = ?".format(filters[colname]), (parameters[value],))
    #sql = "SELECT * FROM switzerland_new WHERE name = :name" 
    sql="SELECT * FROM switzerland_new WHERE {} IN ('{}')".format(colname, value)
    #sql="SELECT * FROM switzerland_new WHERE {} IN %s".format(colname,value)
    #args = [(value,)] # Don't forget the "comma", to force the tuple
    #result =pd.read_sql_query(sql.format(colname, value),con=alchemyEngine)
    #result =pd.read_sql_query(sql.format(colname, value),con=alchemyEngine)
    result =alchemyEngine.execute(sql)
    return(result)


from math import radians, cos, sin, asin, sqrt
def dist(lat1, long1, lat2, long2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])
    # haversine formula 
    dlon = long2 - long1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km
    
def closest_point(latitude,longitude):
    df=pd.read_sql_query('select * from \"switzerland_new\"',con=alchemyEngine)
    distances = df.apply(lambda row: dist(latitude, longitude, row['lon'], row['lat']), axis=1)
    return(df.loc[distances.idxmin()])
 #   df=pd.read_sql_query("SELECT ST_Distance(distance, 'SRID=26910;POINT(latitude longitude)') AS closest_pt FROM switzerland_new ORDER BY distance",con=alchemyEngine)
 #   print("####################done")
 #   return df

