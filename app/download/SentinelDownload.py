from datetime import date
from pathlib import Path
from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt
import yaml

# Open yaml 
home_path = str(Path.home())
yaml_path = str(Path('workspace/harpia/app/config/const.yaml'))
yaml_path = f'{home_path}/{yaml_path}'

with open(yaml_path, 'r') as f:
        const = yaml.load(f)

user = const['data_hub']['user']
password = const['data_hub']['password']

# connect to the API
api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')


# search by polygon, time, and Hub query keywords
geojson_path = str(Path('workspace/harpia/app/download/baixo_sul.geojson'))
geojson_path = f'{home_path}/{geojson_path}'
footprint = geojson_to_wkt(read_geojson(geojson_path))

products = api.query(footprint,
                     date = ('2017516', '20181231'),
                     platformname = 'Sentinel-2',
                     cloudcoverpercentage = (0, 20))

# GeoPandas GeoDataFrame with the metadata of the scenes and the footprints as geometries
df = api.to_geodataframe(products)
df.to_csv(Path('app/download/2017516_20181231_LXN_LXM.csv'))

# download all results from the search
directory_path = 'BRUTA/Sentinel2'
directory_path = f'{home_path}/{directory_path}'

api.download_all(products, directory_path=directory_path)
