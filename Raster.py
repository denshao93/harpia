import glob
import gdal
import numpy as np


class Raster:

    def __init__(self, raster_folder):
        self.raster_folder = raster_folder

    def get_stack_all_bands(self):

        b1 = gdal.Open(glob.glob(self.raster_folder + '/**B1.TIF')[0])\
            .ReadAsArray()  # Costal Aerosol
        b2 = gdal.Open(glob.glob(self.raster_folder + '/**B2.TIF')[0])\
            .ReadAsArray()  # Blue
        b3 = gdal.Open(glob.glob(self.raster_folder + '/**B3.TIF')[0])\
            .ReadAsArray()  # Green
        b4 = gdal.Open(glob.glob(self.raster_folder + '/**B4.TIF')[0])\
            .ReadAsArray()  # Red
        b5 = gdal.Open(glob.glob(self.raster_folder + '/**B5.TIF')[0])\
            .ReadAsArray()  # NIR
        b6 = gdal.Open(glob.glob(self.raster_folder + '/**B6.TIF')[0])\
            .ReadAsArray()  # SWIR1
        b7 = gdal.Open(glob.glob(self.raster_folder + '/**B7.TIF')[0])\
            .ReadAsArray()  # SWIR2
        b9 = gdal.Open(glob.glob(self.raster_folder + '/**B9.TIF')[0])\
            .ReadAsArray()  # Cirrus

        # Create RGB
        np_stack = np.dstack((b1, b2, b3, b4, b5, b6, b7, b9))
        del b1, b2, b3, b4, b5, b6, b7, b9

        return np_stack

    def plot_3d_array(self, r, g, b):
        """
        Atentar para a indexação no array (começa em 0)
        :param r:
        :param g:
        :param b:
        :return:
        """

        # Extract reference to SWIR1, NIR, and Red bands
        index = np.array([r, g, b])
        colors = self.get_stack_all_bands()[:, :, index].astype(np.float64)

        max_val = 64000
        min_val = 0

        # Enforce maximum and minimum values
        colors[colors[:, :, :] > max_val] = max_val
        colors[colors[:, :, :] < min_val] = min_val

        for b in range(colors.shape[2]):
            colors[:, :, b] = colors[:, :, b] * 1 / (max_val - min_val)

        return colors
