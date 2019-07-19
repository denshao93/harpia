import datetime
from collections import OrderedDict
from os import mkdir
from os.path import exists, join
from pathlib import Path

import geopandas as gpd
import yaml
from geopandas_postgis import PostGIS
from sentinelsat import SentinelAPI
from sqlalchemy import create_engine

import ConnectionDB as C

FOLDER_NAME = 'BRUTA_DEV'

path_home = Path.home()

# Open yaml 
with open(Path("app/config/const.yaml"), 'r') as f:
        const = yaml.safe_load(f)

# Open Datahub parameters
data_hub = const['data_hub']

conn_string = const['db']

def list_img2download(conn_string: str, schema: str, table: str):
    con = C.Connection(conn_string)
    query = f"SELECT uuid FROM {schema}.{table} WHERE date_download_img IS NULL"
    try:
        list_uuid = [i[0] for i in con.run_query(query)]
        return list_uuid
    except TypeError as error:
        print(error)


def get_title(conn_string: str, schema: str, table: str, uuid:str):
    con = C.Connection(conn_string)
    query = f"SELECT title FROM {schema}.{table} WHERE uuid = '{uuid}'"
    try:
        title = con.run_query(query)[0][0]
        return title
    except TypeError as error:
        print(error)


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
    if not exists(dst_folder):
        try:
            mkdir(dst_folder)
            return dst_folder
        except:
            raise FileExistsError(f"Can't create destination directory {dst_folder}")
    else:
        return dst_folder
    

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
        
    if exists(join(folder, file_name+file_extention+'.incomplete')):
        return False
    else:
        file_path = join(folder, file_name+file_extention)
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


def dowload_img(list_index, dst_folder):
    # connect to the API
    api = SentinelAPI(data_hub['user'], data_hub['password'], 'https://scihub.copernicus.eu/dhus')
    for i in list_index: 
        
        title = get_title(conn_string, schema='metadado_img', table='metadado_sentinel', uuid=i)
        
        file_already_download = is_file_in_folder(folder=path_home/'BRUTA_DEV', file_name=title, file_extention='.zip') 
        
        if file_already_download:
            insert_date_hour_db(conn_string=conn_string, schema='metadado_img', 
                            table='metadado_sentinel',column='date_download_img', 
                            uuid=i)
        else:
            api.download(i, directory_path=dst_folder)
            insert_date_hour_db(conn_string=conn_string, schema='metadado_img', 
                            table='metadado_sentinel',column='date_download_img', 
                            uuid=i)
           

dst_folder = path_output_folder(FOLDER_NAME)
list_index = list_img2download(conn_string, 'metadado_img', 'metadado_sentinel')

dowload_img(list_index, dst_folder)