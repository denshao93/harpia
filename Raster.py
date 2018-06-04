import os
import gdal
import rasterio
import numpy as np
import geo_utils as gu


class Raster:

    def __init__(self, image_path):

        self.image_path = image_path

    def read_image(self):

        image = rasterio.open(self.image_path)

        return image

    def get_espg_image(self):

        epsg = self.read_image().crs

        return epsg
        
    def bounds_raster(self):

        bbox = self.read_image().bounds

        return bbox

    def bounds_raster_polygon(self):

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

if __name__ == '__main__':

    r = Raster("../../Documents/LC08_L1TP_215069_20161015_20170319_01_T1/LC08_L1TP_215069_20161015_20170319_01_T1_B1.TIF")

    src = r.read_image()
    print(r.bounds_raster_polygon())