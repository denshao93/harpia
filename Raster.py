import os
from geomet import wkt
import shapefile
from osgeo import gdal
import rasterio
import rasterio.features
import shapely
import pprint
import numpy as np
import geo_utils as gu


class Raster:

    def __init__(self, img_path):

        self.image_path = img_path
        # self.dir_img_path = dir_img_path

    def read_image(self):

        image = rasterio.open(self.image_path)

        return image

    def _bounds_raster_polygon(self):

        # Read the input raster into a Numpy array
        infile = self.image_path
        data   = gdal.Open(infile)
        arr1    = data.ReadAsArray()

        # Do some processing....
        arr = arr1 > 0

        arr = arr.astype('uint8')
        # Save out to a GeoTiff

        # First of all, gather some information from the original file
        [cols,rows] = arr.shape
        trans       = data.GetGeoTransform()
        proj        = data.GetProjection()
        # nodatav     = data.GetNoDataValue()
        outfile     = os.path.join("../../Documents/", "outputfile.tif")


        shapes = rasterio.features.shapes(arr)
        polygons = [shapely.geometry.Polygon(shape[0]["coordinates"][0]) for shape in shapes if shape[1] == 1]

        # Create the file, using the information from the original file
        outdriver = gdal.GetDriverByName("GTiff")
        outdata   = outdriver.Create(str(outfile), rows, cols, 1, gdal.GDT_Byte)

        # Write the array to the file, which is the original array in this example
        outdata.GetRasterBand(1).WriteArray(arr)

        # Set a no data value if required
        # outdata.GetRasterBand(1).SetNoDataValue(nodatav)

        # Georeference the image
        outdata.SetGeoTransform(trans)

        # Write projection information
        outdata.SetProjection(proj)

    def _bounds_raster_polygon_geom(self):

        # Read the input raster into a Numpy array
        infile = self.image_path
        data   = gdal.Open(infile)
        arr1    = data.ReadAsArray()

        # Do some processing....
        arr = arr1 > 0

        arr = arr.astype('uint8')
        import matplotlib.pyplot as plt
        # plt.imshow(arr)
        # plt.show()

        # Read the dataset's valid data mask as a ndarray.
        # First of all, gather some information from the original file
        trans       = data.GetGeoTransform()
        proj        = data.GetProjection()
        print(proj)
        # Extract feature shapes and values from the array.
        import rasterio.features as features
        import pandas as pd
        from geopandas import GeoDataFrame
        from shapely.geometry import shape
        d = {}
        d['val']=list()
        geometry = list()

        for shp, val in features.shapes(arr):
            if val == 1:
                d['val'].append(val)
                print(shape(shp).to_wkt())
                geometry.append(shape(shp))
                print(val)
            # print('%s: %s' % (val, shape(shp)))
        df = pd.DataFrame(data=d)
        geo_df = GeoDataFrame(df,crs={'init': 'EPSG:32624'},geometry = geometry)
        geo_df['area'] =  geo_df.area
        geo_df.plot()
        plt.show()
        print(trans)



        # shapes = rasterio.features.shapes(arr, connectivity=8)
        # polygons = [shapely.geometry.Polygon(shape[0]["coordinates"][0]) for shape in shapes if shape[1] == 1]

        # print(wkt.dumps(shape,decimals=2))
        # return polygons

    # def trace_outline_from_raster_shapefile(self):

    #     try:
    #         vct_output = os.path.join(self.dir_img_path, "trace_outline.shp")
    #         if os.path.isfile(vct_output) is not True:

    #             command = "gdal_trace_outline {img_input} -ndv 0 -out-cs en -dp-toler 10 " \
    #             "-ogr-out {vct_output}".format(img_input=self.image_path, vct_output=vct_output)

    #             os.system(command)
    #     except Exception:
    #         print("Problem to run gdal_trace_outline")

    # def trace_outline_raster_poly_geom(self):

    #     vector = os.path.join(self.dir_img_path, "trace_outline.shp")

    #     shp_geom = gu.read_shapefile_poly(vector)

    #     return shp_geom

if __name__ == "__main__":

    Raster(img_path="/media/diogocaribe/56A22ED6A22EBA7F/BRUTA/LANDSAT/" \
    "LC08_L1TP_215068_20171205_20171222_01_T1/" \
    "LC08_L1TP_215068_20171205_20171222_01_T1_B1.TIF")._bounds_raster_polygon_geom()