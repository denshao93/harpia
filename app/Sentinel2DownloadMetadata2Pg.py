import datetime
from collections import OrderedDict
from os.path import exists, join
from pathlib import Path

import geopandas as gpd
import yaml
from geopandas_postgis import PostGIS
from sentinelsat import SentinelAPI
from sqlalchemy import create_engine

import ConnectionDB as C

# Open yaml 
with open(Path("app/config/const.yaml"), 'r') as f:
        const = yaml.safe_load(f)

# Open Datahub parameters
data_hub = const['data_hub']

conn_string = const['db']

# connect to the API
api = SentinelAPI(data_hub['user'], data_hub['password'], 'https://scihub.copernicus.eu/dhus')

query_kwargs = {
        'platformname': 'Sentinel-2',
        'producttype': 'S2MSI1C', 
        'cloudcoverpercentage': (0, 100),
        'date': ('20160101', '20191201'),
        'limit': 20} # date: begindate enddate (ex. 'NOW-14DAYS', 'NOW')

tiles = ['24LVJ']
products = OrderedDict()
for tile in tiles:
    kw = query_kwargs.copy()
    kw['tileid'] = tile 
    pp = api.query(**kw)
    products.update(pp)

# GeoPandas GeoDataFrame with the metadata of the scenes and the footprints as geometries
gdf = api.to_geodataframe(products)


def metadata_img_is_saved_db(conn_string: str, schema: str, table: str, uuid: str):
    """Check is metadado from satellite image was saved in postgres database.
    
    Arguments:
        conn_string {str} -- String to connect to postgres database 
             conn_stromg --> host=localhost dbname=dbname user=user_db password=password_db port=5432
        schema {str} -- shcema name
        table {str} -- table name from schema
        uuid {str} -- single identification of sentinel satellite 2 image 
    
    Returns:
        [bool] -- The return value. True if file has metadata saved in database 
                table, False otherwise.
    """
    # Connect to Database
    con = C.Connection(conn_string)
    query = f"SELECT uuid FROM {schema}.{table} WHERE index = '{uuid}'"
    try:
        metadado_was_saved_db = (len(con.run_query(query)) == 1)
        return metadado_was_saved_db
    except TypeError as error:
        print(error)


def load_sentinel_metadata_db(gdf, engine):
    
    for i in range(0, len(gdf)):
        
        uuid = gdf['uuid'][i]
        
        # Check if file was downloaded anytime
        metadata_save_db = metadata_img_is_saved_db(conn_string=conn_string, 
            schema='metadado_img', table='metadado_sentinel', uuid=uuid)

        # Select row from dataframe
        g = gdf[gdf['uuid'] == uuid].copy()
        
        if not metadata_save_db:
            g.postgis.to_postgis(con=engine, schema='metadado_img', if_exists='append', 
                            table_name='metadado_sentinel', geometry='Polygon')


def create_sqlalchemy_engine(user: str, password: str, host: str, port: int,
                            db_name: str):
    # Create engine to use with sqlalchemy 
    engine_con = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
    engine = create_engine(engine_con)
    return engine

engine = create_sqlalchemy_engine('postgres', 'postgres', 'localhost', 5432, 'harpia')

load_sentinel_metadata_db(gdf, engine)
