

from typing import Union

from fastapi import FastAPI
from utils import *

from fastapi import FastAPI
app = FastAPI()


conn_string = "host='localhost' dbname='Datamodel' user='postgres' password='Gangster30'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

@app.get("/")
async def root():
    return {"message": "Hello World"}



# @app.get("/REGISTER")
# def regions():
#     get_regions=f"http://missilecommand.live:8080/REGISTER"
#     register = requests.get(get_regions)
#     if register.status_code == 200:
#         register_info=(json.loads(register.content.decode('utf-8')))
#     elif register_info=='No data found':
#        reset= f"http://missilecommand.live:8080/RESET"
#        resetting = requests.get(reset)
#        register = requests.get(get_radarsweep)
#     else:
#         register='No data found'    
#     return(register)  
  

@app.get("/START/{team_id}")
def teamID():
    team_id=4
    return(team_id)



@app.get("/region")
def region(numRegions : int = 6,id : int = -1):
    if id < 0:
        where = " "
    else:
        where = f" WHERE cid = {id}"
    sql = f"SELECT cid,geom::json FROM public.regions_{numRegions} {where}"
    print(sql)
    res = conn.queryOne(sql)
    print(res['data'][:2])
    fc = {
        "type": "FeatureCollection",
        "features": []
    }
    feature = {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": None
      }
    }
    return fc

    
    
@app.get("/radar_sweep")
def radar_sweep():
    get_radarsweep=f"http://missilecommand.live:8080/RADAR_SWEEP"
    radar = requests.get(get_radarsweep)
    if radar.status_code == 200:
        radar_info=(json.loads(radar.content.decode('utf-8')))
    else:
        radar_info='No data found'
    return(radar_info)



@app.get("/Fire_Solution")
def Fire_Solution():
    solution=expected_response()
    return(solution)



@app.get("/missile_path")
def missilePath(d: str = None, buffer: float = 0):
    """ Returns a missile path across the entire continental US 
        **Not sure how necessary this is:)**
    ### Params:
        d (str) : direction of missile, if None then it will be random
        buffer (float) : a padding added to or from the bbox (Cont US)
    ### Returns:
        [float,float] start and end
    """
    bbox = {
        "l": -124.7844079,  # left
        "r": -66.9513812,   # right
        "t": 49.3457868,    # top
        "b": 24.7433195,    # bottom
    }

    directions = ["N", "S", "E", "W"]

    if not d:
        d = random.shuffle(directions)

    x1 = ((abs(bbox["l"]) - abs(bbox["r"])) * random.random() + abs(bbox["r"])) * -1
    x2 = ((abs(bbox["l"]) - abs(bbox["r"])) * random.random() + abs(bbox["r"])) * -1
    y1 = (abs(bbox["t"])  - abs(bbox["b"])) * random.random() + abs(bbox["b"])
    y2 = (abs(bbox["t"])  - abs(bbox["b"])) * random.random() + abs(bbox["b"])

    if d == "N":
        start = [x1, bbox["b"] - buffer]
        end = [x2, bbox["t"] + buffer]
    elif d == "S":
        start = [x1, bbox["t"] + buffer]
        end = [x2, bbox["b"] - buffer]
    elif d == "E":
        start = [bbox["l"] - buffer, y1]
        end = [bbox["r"] + buffer, y2]
    else:
        start = [bbox["r"] + buffer, y1]
        end = [bbox["l"] - buffer, y2]

    return [start, end]


@app.get("/missileInfo")
def missileInfo(name: str = None):
    """Get the speed and blast radius for the arsenal of missiles.
    ### Params:
        name (str) : filter the results to match name. Otherwise all missiles are returned.
    ### Returns:
        (list) : one or all missiles
    """

    where = ""

    if name:
        where = f"WHERE missile_properties.name like '{name}'"

    sql = f"""
        SELECT
        missile_properties.name,
        missile_properties.ms,
        missile_properties.blast_radius
        FROM
        missile_properties
        {where}
    """

    print(sql)

    res = cur.execute(sql)
    conn.commit()
    cur.close()
    returnVals = []
    
    for row in res['data']:
        returnVals.append({"name":row[0],"speed":row[1],"blast":row[2]})
    return returnVals


@app.get("/missileNext")
def missileNext(lon:float=-98.12345, lat:float=34.2345, speed:float=333, bearing:float=270, time:int=1, drop:float=0.0 , geojson:bool=False):
    """
    lon (float) : x coordinate
    lat (float) : y coordinate
    speed (int) : meters per second
    bearing (float) : direction in degrees (0-360)
    """
    if not geojson:
        select = "lon1 as x1, lat1 as y1, st_x(p2) as x2,st_y(p2) as y2"
    else:
        select = "ST_AsGeoJSON(p2)"

    sql = f"""
    WITH 
        Q1 AS (
            SELECT {lon} as lon1,{lat} as lat1, ST_SetSRID(ST_Project('POINT({lon} {lat})'::geometry, {speed*time}, radians({bearing}))::geometry,4326) as p2
        )
 
    SELECT {select}
    FROM Q1
    """

    print(sql)

    res = cur.execute(sql)

    cleanResult = {
        "lon1":res['data'][0],
        "lat1":res['data'][1],
        "lon2":res['data'][2],
        "lat2":res['data'][3]
    }

    res['data'] = cleanResult
    return res
