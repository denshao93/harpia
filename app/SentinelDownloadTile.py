import datetime
from collections import OrderedDict
from os.path import exists, join
from pathlib import Path

import geopandas as gpd
from geopandas import GeoDataFrame
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

# connect to the API
api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')


query_kwargs = {
        'platformname': 'Sentinel-2',
        'producttype': 'S2MSI1C', # producttype
        'cloudcoverpercentage': (0, 1), # cloudcoverpercetage (min, max)
        'date': ('20170101', '20171201')} # date: begindate enddate (ex. 'NOW-14DAYS', 'NOW')

tiles = ['24LVJ'] # *tiles
products = OrderedDict()
for tile in tiles:
    kw = query_kwargs.copy()
    kw['tileid'] = tile 
    pp = api.query(**kw)
    products.update(pp)

# GeoPandas GeoDataFrame with the metadata of the scenes and the 
# footprints as geometries
gdf = api.to_geodataframe(products)

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

def metadata_img_is_saved_db(conn_string: str, schema: str, table: str, uuid: str):
    """Check is metadado from satellite image was saved in postgres database.
    
    Example:
        conn_strig --> host=localhost dbname=dbname user=user_db password=password_db port=5432

    Arguments:
        conn_string {str} -- String to connect to postgres database 
        schema {str} -- shcema name
        table {str} -- table name from schema
        uuid {str} -- single identification of sentinel satellite 2 image 
    
    Returns:
        [bool] -- The return value. True if file has metadata saved in database table, False otherwise.
    """
    # Connect to Database
    con = C.Connection(const['harpia_db'])
    query = f"SELECT index FROM {schema}.{table} WHERE index = '{uuid}'"
    metadado_was_saved_db = (len(con.run_query(query)) == 1)
    return metadado_was_saved_db

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


def load_metadata_db(geodataframe: GeoDataFrame, conn_string: str, schema: str, 
                    table_name: str, geometry: str, if_exists='append'):
    """Load metadata (geodataframe) in postgres database.
    
    Exemples:
    ----------
    conn_string:
        host=localhost dbname=dbname user=user_db password=password_db port=5432
    Parameters
    ----------
    geopandas : GeoDataFrame
        Table with alphanumeric data and image footprint as GeoDataframe
    conn_string : str
        String to connect to postgres database
    schema : str
        Schema name
    table_name : str
        Table name
    geometry : str
        The kind of geometry (Polygon, Multipolygon)
    if_exists : str, optional
        If table exist in schema database the date will be store, 
        by default 'append'.
    """
    con = C.Connection(conn_string)
    engine = create_engine('postgresql://', creator=con.open_connect())
    geodataframe.postgis.to_postgis(con=engine, schema='metadado_img', 
            if_exists='append', table_name='metadado_sentinel', geometry='Polygon')


dst_folder = path_output_folder(FOLDER_NAME)
for i in range(0, len(gdf)):
    uuid = gdf['uuid'][i] 
    
    file_name = gdf['title'][i]
    file_exist = is_file_in_folder(FOLDER_NAME, file_name, file_extention='.zip')

    # Check if file was downloaded anytime
    metadata_is_save_db = metadata_img_is_saved_db(conn_string=const['harpia_db'], 
        schema='metadado_img', table='metadado_sentinel', uuid=uuid)

    # Select the line of geodataframe
    g = gdf[gdf['uuid'] == uuid].copy()
    if not file_exist and not metadata_is_save_db:
        # Set time value where file was downloaded
        g.loc[0, 'date_download'] = datetime.datetime.now()
        # Downlod file
        api.download(uuid, directory_path=dst_folder)
        # Load metadata in database
        load_metadata_db(geodataframe=g, conn_string=const['harpia_db'], 
                        schema='metadado_img', table_name='metadado_sentinel', 
                        geometry='Polygon')

    elif file_exist and not metadata_is_save_db:
        load_metadata_db(geodataframe=g, conn_string=const['harpia_db'], 
                        schema='metadado_img', table_name='metadado_sentinel', 
                        geometry='Polygon')

# Create table in order save 
'''
DROP SCHEMA metadado_img CASCADE;
CREATE SCHEMA metadado_img;
DROP SEQUENCE metadado_sentinel_id_seq CASCADE;

CREATE SEQUENCE metadado_sentinel_id_seq;

-- GRANT USAGE ON SCHEMA metadado_img TO grp_consulta;

-- GRANT ALL ON SCHEMA metadado_img TO tmzuser;

-- Table: metadado_img.metadado_sentinel

-- DROP TABLE metadado_img.metadado_sentinel;

CREATE TABLE metadado_img.metadado_sentinel
(
    index text COLLATE pg_catalog."default",
    title text COLLATE pg_catalog."default",
    link text COLLATE pg_catalog."default",
    link_alternative text COLLATE pg_catalog."default",
    link_icon text COLLATE pg_catalog."default",
    summary text COLLATE pg_catalog."default",
    datatakesensingstart timestamp without time zone,
    beginposition timestamp without time zone,
    endposition timestamp without time zone,
    ingestiondate timestamp without time zone,
    orbitnumber bigint,
    relativeorbitnumber bigint,
    cloudcoverpercentage double precision,
    sensoroperationalmode text COLLATE pg_catalog."default",
    tileid text COLLATE pg_catalog."default",
    hv_order_tileid text COLLATE pg_catalog."default",
    format text COLLATE pg_catalog."default",
    processingbaseline text COLLATE pg_catalog."default",
    platformname text COLLATE pg_catalog."default",
    filename text COLLATE pg_catalog."default",
    instrumentname text COLLATE pg_catalog."default",
    instrumentshortname text COLLATE pg_catalog."default",
    size text COLLATE pg_catalog."default",
    s2datatakeid text COLLATE pg_catalog."default",
    producttype text COLLATE pg_catalog."default",
    platformidentifier text COLLATE pg_catalog."default",
    orbitdirection text COLLATE pg_catalog."default",
    platformserialidentifier text COLLATE pg_catalog."default",
    processinglevel text COLLATE pg_catalog."default",
    identifier text COLLATE pg_catalog."default",
    uuid text COLLATE pg_catalog."default",
    geom geometry(Polygon,4326),
    id integer NOT NULL DEFAULT nextval('metadado_sentinel_id_seq'::regclass),
    date_download timestamp without time zone,
    level1cpdiidentifier character(250) COLLATE pg_catalog."default",
    is_download boolean,
    is_processed boolean,
    file_path boolean
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE metadado_img.metadado_sentinel
    OWNER to tmzuser;

-- GRANT SELECT ON TABLE metadado_img.metadado_sentinel TO grp_consulta;

-- GRANT ALL ON TABLE metadado_img.metadado_sentinel TO tmzuser;

-- Index: idx_metadado_sentinel_geom

-- DROP INDEX metadado_img.idx_metadado_sentinel_geom;

CREATE INDEX idx_metadado_sentinel_geom
    ON metadado_img.metadado_sentinel USING gist
    (geom)
    TABLESPACE pg_default;

-- Index: idx_metadado_sentinel_index

-- DROP INDEX metadado_img.idx_metadado_sentinel_index;

CREATE INDEX idx_metadado_sentinel_index
    ON metadado_img.metadado_sentinel USING btree
    (index COLLATE pg_catalog."default", id)
    TABLESPACE pg_default;
'''
