import yaml
from pathlib import Path
from datetime import date
from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt


# Open yaml 
with open(Path("config/const.yaml"), 'r') as f:
        const = yaml.load(f)

user = const['data_hub']['user']
password = const['data_hub']['password']

# connect to the API
api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')

# download single scene by known product id
# api.download(<product_id>)

# search by polygon, time, and Hub query keywords
footprint = geojson_to_wkt(read_geojson(Path('download/baixo_sul.geojson')))
products = api.query(footprint,
                     date = ('20180801', '20180830'),
                     platformname = 'Sentinel-2',
                     producttype = "S2MSI1C",
                     cloudcoverpercentage = (0, 30),
                     limit=1)
print(products)

# download all results from the search
api.download_all(products, directory_path='~/BRUTA/Sentinel2A/')