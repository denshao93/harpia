from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date

# connect to the API
api = SentinelAPI('dogosousa', 'ana220879', 'https://scihub.copernicus.eu/dhus')

# download single scene by known product id
# api.download(<product_id>)

# search by polygon, time, and Hub query keywords
footprint = geojson_to_wkt(read_geojson("/home/diogocaribe/workspace/harpia/app/download/baixo_sul.geojson"))
products = api.query(footprint,
                     date = ('20180801', '20180830'),
                     platformname = 'Sentinel-2',
                     producttype = "S2MSI1C",
                     cloudcoverpercentage = (0, 30))

# download all results from the search
api.download_all(products, directory_path='/home/diogocaribe/Downloads')