import matplotlib.pyplot as plt
import gdal

from skimage.segmentation import felzenszwalb, slic, quickshift
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
from skimage import io

image = 'LC08_L1TP_215068_20151114_20170402_01_T1/PROCESSADA/clip_LC08_L1TP_215068_20151114_20170402_01_T1.tif'


img = io.imread(image)
segments = quickshift(img, kernel_size=10, convert2lab=False, max_dist=6, ratio=0.5)
plt.imshow(segments)