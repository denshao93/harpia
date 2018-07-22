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
        # self.dir_img_path = dir_img_path

    def read_image(self):

        image = rasterio.open(self.image_path)

        return image

    def trace_outline_from_raster_wkt(self):

        with rasterio.open(self.image_path) as dataset:

            # Read the dataset's valid data mask as a ndarray.
            mask = dataset.dataset_mask()
            
            # Extract feature shapes and values from the array.
            for geom, val in rasterio.features.shapes( #NOQA
                    mask, transform=dataset.transform):

                # Transform shapes from the dataset's own coordinate
                # reference system to SIRGAS 2000 (EPSG:4674).
                geom = rasterio.warp.transform_geom(
                    dataset.crs, 'EPSG:4674', geom, precision=6)

                # Print Polygon Wkt shapes to stdout.
                trace_outline = shape(geom).to_wkt()

                return trace_outline
                
    def trace_outline_from_raster_shapefile(self):

        try:
            vct_output = os.path.join(self.image_path, "trace_outline.shp")
            if os.path.isfile(vct_output) is not True:

                command = "gdal_trace_outline {img_input} -ndv 0 -out-cs en -dp-toler 10 " \
                "-ogr-out {vct_output}".format(img_input=self.image_path, vct_output=vct_output)

                os.system(command)
        except Exception:
            print("Problem to run gdal_trace_outline")

    def trace_outline_raster_poly_geom(self):

        vector = os.path.join(self.image_path, "trace_outline.shp")

        shp_geom = gu.read_shapefile_poly(vector)

        return shp_geom

if __name__ == "__main__":

    Raster(img_path=f"/tmp/tmp2qtqk6i6/" \
                    f"LC08_L1TP_215068_20171205_20171222_01_T1.TIF")\
                    .trace_outline_from_raster_wkt()
