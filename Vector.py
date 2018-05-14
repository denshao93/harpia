import os
from osgeo import ogr


class Vector:

    def __init__(self, shapefile_path):
        """Class to read and get vector proprieties from vector files

        Arguments:
            shapefile_path {string} -- Place where shape file can be seted
        """
        self.shapefile_path = os.path.abspath(shapefile_path)

    def read_shape_file_ogr(self):
        """Reading vector (.shp) with ogr

        Returns:
            [ogr 0bjet] -- [description]
        """
        file = ogr.Open(self.shapefile_path)
        layer = file.GetLayer(0)

        return layer

    def get_srid_vector(self):
        """Getting srid from vector file

        Returns:
            [str] -- Value from SRID
        """
        driver = ogr.GetDriverByName('ESRI Shapefile')
        dataset = driver.Open(self.shapefile_path)

        # from Layer
        layer = dataset.GetLayer()
        spatialRef = layer.GetSpatialRef()
        print(spatialRef.crs.proj4())

        return spatialRef

    def reproject_layer(self, source_epsg, target_epsg):
        pass

if __name__ == '__main__':

    v = Vector(shapefile_path="vetor/lc8_ba_4674_buffer.shp")

    print(v.get_srid_vector())