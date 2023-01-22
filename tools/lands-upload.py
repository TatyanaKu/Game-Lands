import json
from shapely.geometry import shape
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData
from geoalchemy2 import Geometry


engine = create_engine('postgresql://game-lands:game-lands@192.168.0.3:5432/game-lands', echo=True)  


metadata = MetaData()
land_table = Table('land', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('description', String),
    Column('land_type', String),             
    Column('geom', Geometry('POLYGON'))
)    

land_table.create(engine)


with open('polygon.geojson', 'r', encoding='utf-8') as f:
    data = json.load(f)
    for feat in data['features']:
        g2 = shape(feat['geometry'])
        print(g2.wkt)
        print(feat['properties']['Name'])
        print(feat['properties']['Description'])
        ins = land_table.insert().values(id=int,
                                         name=str,
                                         description=str,
                                         land_type=str,
                                         geom='POLYGON((0 0,1 0,1 1,0 1,0 0))')
        str(ins)

#INSERT INTO lake (name, geom) VALUES (:name, ST_GeomFromEWKT(:geom))