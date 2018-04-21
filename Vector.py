import os
import ogr


class Vector:

    def __init__(self, shapefile_path):
        """Class to read and get vector proprieties from vector files
        
        Arguments:
            shapefile_path {string} -- Place where shape file can be seted
        """
        self.shapefile_path = shapefile_path

    def read_shape_file_ogr(self):
        """Reading vector (.shp) with ogr
        
        Returns:
            [ogr 0bjet] -- [description]
        """
        file = ogr.Open(self.shapefile_path)
        layer = file.GetLayer(0)

        return layer


def get_srid_vector():
    """Getting srid from vector file
    
    Returns:
        [strig] -- Value from SRID 
    """t

    # use Shapefile driver
    driver = ogr.GetDriverByName("ESRI Shapefile")
    # reference Shapefile
    shp = "/media/dogosousa/1AF3820C0AA79B17/PROCESSADA/LC08/2017/12/215068/LC08_L1TP_215068_20171205_20171222_01_T1/LC08_L1TP_215068_20171205_20171222_01_T1.shp"
    # open the file
    ds = driver.Open(shp, 0)
    # reference the only layer in a Shapefile
    lyr = ds.GetLayer(0)
    print(lyr.GetSpatialRef())

    # projected coordinate system
    # proj_string = lyr.GetSpatialRef().GetAttrValue("PROJCS", 0)
    # geographic coordinate system
    # geog_string = lyr.GetSpatialRef().GetAttrValue("GEOGCS", 0)
    # EPSG Code if available
    epsg = lyr.GetSpatialRef().GetAttrValue("AUTHORITY", 1)
    # datum
    datum = lyr.GetSpatialRef().GetAttrValue("DATUM", 0)

    print("\nFile: {0}\n\nProjected: {1}\nEPSG: {2}\n".format(lyr.GetName(),proj_string, epsg))
    print("Geographic: {0}\nDatum: {1}\n".format(geog_string, datum))


if __name__ == '__main__':
    
    get_srid_vector()

