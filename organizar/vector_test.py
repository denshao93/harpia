import ogr


def main():
    # use Shapefile driver
    driver = ogr.GetDriverByName("ESRI Shapefile")
    # reference Shapefile
    # shp = "../../../../media/dogosousa/1AF3820C0AA79B17/PROCESSADA/LC08/2017/12/215068/LC08_L1TP_215068_20171205_20171222_01_T1/LC08_L1TP_215068_20171205_20171222_01_T1.shp"
    shp = "../../Downloads/lc8_ba.shp"
    # open the file
    ds = driver.Open(shp, 0)
    # reference the only layer in a Shapefile
    lyr = ds.GetLayer(0)

    print(lyr.GetSpatialRef())

    # projected coordinate system
    proj_string = lyr.GetSpatialRef().GetAttrValue("PROJCS", 0)
    # geographic coordinate system
    geog_string = lyr.GetSpatialRef().GetAttrValue("GEOGCS", 0)
    # EPSG Code if available
    epsg = lyr.GetSpatialRef().GetAttrValue("AUTHORITY", 1)
    # datum
    datum = lyr.GetSpatialRef().GetAttrValue("DATUM", 0)

    print(proj_string, geog_string, epsg,datum)


if __name__ == '__main__':
    main()