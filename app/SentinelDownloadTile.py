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

FOLDER_NAME = 'BRUTA_DEV'

# Open yaml 
with open(Path("app/config/const.yaml"), 'r') as f:
        const = yaml.safe_load(f)

# Open Datahub parameters
data_hub = const['data_hub']
user = data_hub['user'] # user_hub
password = data_hub['password'] # password_hub

conn_string = "".join(const['harpia_db_dev'])

# connect to the API
api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')


query_kwargs = {
        'platformname': 'Sentinel-2',
        'producttype': 'S2MSI1C', 
        'cloudcoverpercentage': (0, 100), # cloudcoverpercetage (min, max)
        'date': ('20160101', '20191201')} # date: begindate enddate (ex. 'NOW-14DAYS', 'NOW')

tiles = ['24LVJ'] # *tiles
products = OrderedDict()
for tile in tiles:
    kw = query_kwargs.copy()
    kw['tileid'] = tile 
    pp = api.query(**kw)
    products.update(pp)

# GeoPandas GeoDataFrame with the metadata of the scenes and the footprints as geometries
gdf = api.to_geodataframe(products)

# Connect to Database
con = C.Connection(conn_string)


def path_output_folder(folder_name: str):
    """Path of folder where files will store.
    
    Arguments:
        folder_name {str} -- The name of folder where all zip files downloaded
                            from scihub will store.
    
    Returns:
        [str] -- Path of folder
    """
    home_path = str(Path.home())
    dst_folder = join(home_path, folder_name)
    return dst_folder

dst_folder = path_output_folder(FOLDER_NAME)


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
    query = f"SELECT index FROM {schema}.{table} WHERE index = '{uuid}'"
    try:
        metadado_was_saved_db = (len(con.run_query(query)) == 1)
        return metadado_was_saved_db
    except TypeError as error:
        print(error)


def is_file_in_folder(folder: str, file_name: str, file_extention: str):
    """Check if file exist in folder.
    
    Parameters
    ----------
    folder : str
        Folder where file be
    file_name : str
        File name
    file_extention : str
        File extension
    
    Returns
    -------
    [bool]
        If True file be in folder, False otherwise.
    """
    file_path = join(folder, file_name)
    return exists(file_path)


def insert_date_hour_db(conn_string: str, schema: str, table: str, column: str, uuid: str):
    """Update column date_dowload with YYYY/MM/DD and HH:MM:SSSS
    
    Parameters
    ----------
    conn_string : str
        conn_stromg --> host=localhost dbname=dbname user=user_db password=password_db port=5432
    schema : str
        Schema name
    table : str
        Table name
    column : str
        Column name that is saved date and time when file is download.
    uuid : str
        Unique identifier
    """
    con = C.Connection(conn_string)
    query = f"UPDATE {schema}.{table} SET {column} = current_timestamp WHERE uuid = '{uuid}'"
    con.run_query(query)

engine_con = f'postgresql://postgres:postgres@localhost:5432/harpia'
engine = create_engine(engine_con)


def insert_metadata_db(geodataframe, con: str, schema: str, if_exists: str, 
                    table_name: str, geometry: str):
    geodataframe.postgis.to_postgis(con=con, schema=schema, if_exists=if_exists, 
                                    table_name=table_name, geometry=geometry)


def load_sentinel2metadata_pg(gdf):
        
    for i in range(0, len(gdf)):
        
        uuid = gdf['uuid'][i]
        
        # Check if file was downloaded anytime
        metadata_save_db = metadata_img_is_saved_db(conn_string=conn_string, 
            schema='metadado_img', table='metadado_sentinel', uuid=uuid)

        # Selecionando a linha do geodataframe
        g = gdf[gdf['uuid'] == uuid].copy()
        
        if not metadata_save_db:
            print(i)
            insert_metadata_db(g, con=engine, schema='metadado_img', if_exists='append', 
                            table_name='metadado_sentinel', geometry='Polygon')

load_sentinel2metadata_pg(gdf)


# for i in range(0, len(gdf)):
#     uuid = gdf['uuid'][i]
    
#     # File path to know if it exist
#     file_name = gdf['title'][i]
#     file_path = join(dst_folder, f'{file_name}.zip')

#     # Check if file was downloaded anytime
#     metadata_is_save_db = metadata_img_is_saved_db(conn_string=conn_string, 
#         schema='metadado_img', table='metadado_sentinel', uuid=uuid)

#     # Selecionando a linha do geodataframe
#     g = gdf[gdf['uuid'] == uuid].copy()
    
#     if not exists(file_path) and not metadata_is_save_db:
#         # api.download(uuid, directory_path=dst_folder)

#         insert_metadata_db(g, con=engine, schema='metadado_img', if_exists='append', 
#                          table_name='metadado_sentinel', geometry='Polygon')

#         insert_date_hour_db(conn_string=conn_string, schema='metadado_img', table='metadado_sentinel',column='date_download', uuid=uuid)
    
#     elif exists(file_path) and not metadata_is_save_db:
#         insert_metadata_db(g, con=engine, schema='metadado_img', if_exists='append', 
#                          table_name='metadado_sentinel', geometry='Polygon')