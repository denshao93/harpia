import os
import shapefile
from osgeo import gdal
import rasterio
import rasterio.warp
import numpy as np
import geo_utils as gu
import rasterio.features as features
from shapely.geometry import shape

class Raster:

    def __init__(self, img_path):

        self.image_path = img_path


    def read_image(self):

        image = rasterio.open(self.image_path)

        return image

    def trace_outline_from_raster_wkt(self):

        with rasterio.open(self.image_path) as dataset:

            # Read the dataset's valid data mask as a ndarray.
            mask = dataset.dataset_mask()
            
            # Extract feature shapes and values from the array.
            for geom, val in rasterio.features.shapes(
                    mask, transform=dataset.transform):

                # Transform shapes from the dataset's own coordinate
                # reference system to SIRGAS 2000 (EPSG:4674).
                geom = rasterio.warp.transform_geom(
                    dataset.crs, 'EPSG:4674', geom, precision=6)

                # Print Polygon Wkt shapes to stdout.
                trace_outline = shape(geom).to_wkt()

                return trace_outline
       
    def intersects_trace_outline_aoi(self):
        """Verify if image have to be cliped.

        If img overlap boundery of area of interested project (aoi),
        It should be cliped to remove image that not be useless.
        This processing avoid to save raster useless areas.

        """
        ba_line = gu.read_shapefile_poly("/home/diogo.sousa/workspace/harpia/data/vector/ba_4674_line.shp")
        
        from shapely import wkt
        trace_outline = wkt.loads(self.trace_outline_from_raster_wkt())

        intersects = trace_outline.intersects(ba_line)

        return intersects
