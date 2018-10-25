import yaml
from pathlib import Path
from collections import OrderedDict
from sentinelsat import SentinelAPI

# Open yaml 
with open(Path("config/const.yaml"), 'r') as f:
        const = yaml.load(f)

user = const['data_hub']['user']
password = const['data_hub']['password']

# connect to the API
api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')

tiles = ['24LXP']

query_kwargs = {
        'platformname': 'Sentinel-2',
        'producttype': 'S2MSI1C',
        'cloudcoverpercentage': (0, 99),
        'date': ('20180907', '20180909')}

products = OrderedDict()
for tile in tiles:
    kw = query_kwargs.copy()
    kw['tileid'] = tile  # products after 2017-03-31
    pp = api.query(**kw)
    products.update(pp)

# GeoPandas GeoDataFrame with the metadata of the scenes and the footprints as geometries
df = api.to_geodataframe(products)
df.to_csv(Path('app/download/2018.csv')

# download all results from the search
api.download_all(products, directory_path=Path('~/BRUTA/Sentinel2'))
