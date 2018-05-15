""""Clip a raster image using a shapefile"""

from osgeo import gdal, gdalnumeric
import shapefile
from PIL import Image, ImageDraw

# Raster image to clip
raster = "/media/diogocaribe/56A22ED6A22EBA7F/PROCESSADA/LC08/2016/09/215068/LC08_L1TP_215068_20160913_20170321_01_T1/LC08_L1TP_215068_20160913_20170321_01_T1.TIF"

# Polygon shapefile used to clip
shp = "vetor/square_215068"

# Name of clipped raster file(s)
output = "/tmp/tmpteste/cut_ref"

def imageToArray(i):
    """
    Converts a Python Imaging Library array to a gdalnumeric image.
    """
    a=gdalnumeric.numpy.fromstring(i.tobytes(),'b')
    a.shape=i.im.size[1], i.im.size[0]
    return a

def world2Pixel(geoMatrix, x, y):

    """
    Uses a gdal geomatrix (gdal.GetGeoTransform()) to calculate
    the pixel location of a geospatial coordinate
    """
    ulX = geoMatrix[0]
    ulY = geoMatrix[3]
    xDist = geoMatrix[1]
    yDist = geoMatrix[5]
    rtnX = geoMatrix[2]
    rtnY = geoMatrix[4]
    pixel = int((x - ulX) / xDist)
    line = int((ulY - y) / xDist)
    return (pixel, line)

# Load the source data as a gdalnumeric array
srcArray = gdalnumeric.LoadFile(raster)

# Also load as a gdal image to get geotransform (world file) info
srcImage = gdal.Open(raster)
geoTrans = srcImage.GetGeoTransform()

# Use pyshp to open the shapefile
r = shapefile.Reader("%s.shp" % shp)

# Convert the layer extent to image pixel coordinates
minX, minY, maxX, maxY = r.bbox
ulX, ulY = world2Pixel(geoTrans, minX, maxY)
lrX, lrY = world2Pixel(geoTrans, maxX, minY)

# Calculate the pixel size of the new image
pxWidth = int(lrX - ulX)
pxHeight = int(lrY - ulY)

# Multi-band image?
#Check this modification in script in: http://karthur.org/2015/clipping-rasters-in-python.html
try:
    clip = srcArray[:, ulY:lrY, ulX:lrX]

# Nope: Must be single-band
except IndexError:
    clip = srcArray[ulY:lrY, ulX:lrX]


# Create a new geomatrix for the image
geoTrans = list(geoTrans)
geoTrans[0] = minX
geoTrans[3] = maxY

# Map points to pixels for drawing the county boundary
# on a blank 8-bit, black and white, mask image.
pixels = []
for p in r.shape(0).points:
  pixels.append(world2Pixel(geoTrans, p[0], p[1]))
rasterPoly = Image.new("L", (pxWidth, pxHeight), 1)
# Create a blank image in PIL to draw the polygon.
rasterize = ImageDraw.Draw(rasterPoly)
rasterize.polygon(pixels, 0)
# Convert the PIL image to a NumPy array
mask = imageToArray(rasterPoly)

# Clip the image using the mask
clip = gdalnumeric.numpy.choose(mask, (clip, 0)).astype(gdalnumeric.numpy.uint16)

# Save clipping as tiff
gdalnumeric.SaveArray(clip, "%s.tif" % output, format="GTiff", prototype=raster)