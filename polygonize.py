import gdal, ogr, osr
# Thresholded input raster name
src = "/tmp/LC08_L1TP_215068_20151114_20170402_01_T1/classified.tiff"
# Output shapefile name
tgt = "/tmp/LC08_L1TP_215068_20151114_20170402_01_T1/extract.shp"
# OGR layer name
tgtLayer = "extract"
# Open the input raster
srcDS = gdal.Open(src)
# Grab the first band
band = srcDS.GetRasterBand(1)
# Force gdal to use the band as a mask
mask = band
# Set up the output shapefile
driver = ogr.GetDriverByName("ESRI Shapefile")
shp = driver.CreateDataSource(tgt)
# Copy the spatial reference
srs = osr.SpatialReference()
srs.ImportFromWkt(srcDS.GetProjectionRef())
layer = shp.CreateLayer(tgtLayer, srs=srs)
# Set up the dbf file
fd = ogr.FieldDefn( "DN", ogr.OFTInteger )
layer.CreateField(fd)
dst_field = 0
# Automatically extract features from an image!
extract = gdal.Polygonize(band, mask, layer, dst_field, [], None)