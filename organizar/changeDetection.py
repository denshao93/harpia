"""Perform a simple difference image change detection on a
'before' and 'after' image."""
from osgeo import gdal, gdalnumeric
import numpy as np

# "Before" image
im1 = "/media/diogocaribe/56A22ED6A22EBA7F/PROCESSADA/LC08/2015/11/215068/LC08_L1TP_215068_20151114_20170402_01_T1/LC08_L1TP_215068_20151114_20170402_01_T1.TIF"
# "After" image
im2 = "/media/diogocaribe/56A22ED6A22EBA7F/PROCESSADA/LC08/2016/09/215068/LC08_L1TP_215068_20160913_20170321_01_T1/LC08_L1TP_215068_20160913_20170321_01_T1.TIF"
# Load before and after into arrays
ar1 = gdalnumeric.LoadFile(im1).astype(np.int8)
ar2 = gdalnumeric.LoadFile(im2)[1].astype(np.int8)
# Perform a simple array difference on the images
diff = ar2 - ar1
# Set up our classification scheme to try
# and isolate significant changes
classes = np.histogram(diff, bins=5)[1]
# The color black is repeated to mask insignificant changes
lut = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,255,0],[255,0,0]]
# Starting value for classification
start = 1
# Set up the output image
rgb = np.zeros((3, diff.shape[0], diff.shape[1],), np.int8)
# Process all classes and assign colors
for i in range(len(classes)):
    mask = np.logical_and(start <= diff, diff <= classes[i])
    for j in range(len(lut[i])):
        rgb[j] = np.choose(mask, (rgb[j], lut[i][j]))
    start = classes[i]+1
# Save the output image
gdalnumeric.SaveArray(rgb, "change.tif", format="GTiff", prototype=im2)

