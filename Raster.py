import os
import shapefile
from osgeo import gdal
import rasterio
import numpy as np
import geo_utils as gu


class Raster:

    def __init__(self, dir_img_path, image_path):

        self.image_path = image_path
        self.dir_img_path = dir_img_path

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
        # Save out to a GeoTiff

        # First of all, gather some information from the original file
        [cols,rows] = arr.shape
        trans       = data.GetGeoTransform()
        proj        = data.GetProjection()
        # nodatav     = data.GetNoDataValue()
        outfile     = os.path.join("../../Documents/", "outputfile.tif")

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

    def trace_outline_from_raster_shapefile(self):

        try:
            vct_output = os.path.join(self.dir_img_path, "trace_outline.shp")
            if os.path.isfile(vct_output) is not True:

                command = "gdal_trace_outline {img_input} -ndv 0 -out-cs en -dp-toler 10 " \
                "-ogr-out {vct_output}".format(img_input=self.image_path, vct_output=vct_output)

                os.system(command)
        except Exception:
            print("Problem to run gdal_trace_outline")

    def trace_outline_raster_poly_geom(self):

        vector = os.path.join(self.dir_img_path, "trace_outline.shp")

        shp_geom = gu.read_shapefile_poly(vector)

        return shp_geom