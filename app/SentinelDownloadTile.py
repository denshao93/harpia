from collections import OrderedDict
from os.path import exists, join
from pathlib import Path
import datetime 

import ConnectionDB as C
import geopandas as gpd
import yaml
from geopandas_postgis import PostGIS
from sentinelsat import SentinelAPI
from sqlalchemy import create_engine


# Open yaml 
with open(Path("app/config/const.yaml"), 'r') as f:
        const = yaml.safe_load(f)

# Open Datahub parameters
user = const['data_hub']['user']
password = const['data_hub']['password']

# Database parameters
harpia_db = const['harpia_db']
host = harpia_db['host']
dbname =  harpia_db['dbname']
user_db = harpia_db['user']
password_db = harpia_db['password']
port = harpia_db['port']

# connect to the API
api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')

tiles = ['24LXN', '24LXM', '24LWN', '24LWM', '24LWL', '24LVL', '24LVK']

query_kwargs = {
        'platformname': 'Sentinel-2',
        'producttype': 'S2MSI1C',
        'cloudcoverpercentage': (0, 100),
        'date': ('20180907', '20190415')}

products = OrderedDict()
for tile in tiles:
    kw = query_kwargs.copy()
    kw['tileid'] = tile  # products after 2017-03-31
    pp = api.query(**kw)
    products.update(pp)

# GeoPandas GeoDataFrame with the metadata of the scenes and the footprints as geometries
gdf = api.to_geodataframe(products)

# Connect to Database 
conn_str = f'postgresql://{user_db}:{password_db}@{host}:{port}/{dbname}'
engine = create_engine(conn_str)

conn_string = f'host={host} dbname={dbname} user={user_db} password={password_db} port={port}'
con = C.Connection(conn_string)

home_path = str(Path.home())
dst_folder = join(home_path, 'BRUTA')

for i in range(0, len(gdf)):
    uuid = gdf['uuid'][i] #se existir não realizar o download
        
    # File path to know if it exist
    file_name = gdf['title'][i]
    file_path = join(dst_folder, f'{file_name}.zip')

    # Verificando se o arquivo já foi baixado alguma vez
    query = f"SELECT index FROM sentinel WHERE index = '{uuid}'"
    rs = con.run_query(query)
 
    if not exists(file_path):
        if len(rs) == 0:
            print(file_name)
            # api.download(uuid, directory_path=dst_folder)
            # Selecionando a linha do geodataframe
            gdf['date_download'] = datetime.datetime.now()
            g = gdf[gdf['uuid'] == uuid] 
            g.postgis.to_postgis(con=engine, if_exists='append', 
                            table_name='sentinel', geometry='MultiPolygon')

# Create table in order save 
'''
-- Table: public.sentinel

-- DROP TABLE public.sentinel;

CREATE TABLE public.sentinel
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
    geom geometry(MultiPolygon,4326),
    id integer NOT NULL DEFAULT nextval('sentinel_id_seq'::regclass) ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
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

ALTER TABLE public.sentinel
    OWNER to postgres;

-- Index: idx_sentinel_geom

-- DROP INDEX public.idx_sentinel_geom;

CREATE INDEX idx_sentinel_geom
    ON public.sentinel USING gist
    (geom)
    TABLESPACE pg_default;

-- Index: ix_sentinel_index

-- DROP INDEX public.ix_sentinel_index;

CREATE INDEX ix_sentinel_index
    ON public.sentinel USING btree
    (index COLLATE pg_catalog."default")
    TABLESPACE pg_default;
'''