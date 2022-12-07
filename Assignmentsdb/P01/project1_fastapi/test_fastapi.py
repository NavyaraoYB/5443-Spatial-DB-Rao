from typing import Union

from fastapi import FastAPI
from utils import *

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/findall")
def findall():
    res = do_findall()
    res=res.iloc[:1000,:]
    res=list(res.itertuples(index=False))
    return res

#findOne
#/findone/1299/texas
#Returns a single tuple based on a column name (attribute) and value (e.g id=1299 , or name=texas).

#http://127.0.0.1:8000/get_tuple/?colname=name&value='Switzerland'

@app.get("/get_tuple/")
def read_item(colname:str,value:str):
   res=get_tuple(colname,value)
   return (res)


#http://127.0.0.1:8000/closest_point/?latitude=8.44&longitude=46.8
@app.get("/closest_point/")
def read_item(latitude: float, longitude: float):
    res = closest_point(latitude,longitude)
    return (tuple(list(res)))