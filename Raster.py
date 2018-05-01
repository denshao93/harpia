import rasterio
from osgeo import gdal
import matplotlib.pyplot as plt


class Raster:
    
    def __init__(self, image_path):

        self.image_path = image_path
    
    def read_image(self):

        image = rasterio.open(self.image_path)

        return image
    
    def get_espg_image(self):
        
        image = rasterio.open(self.image_path)
        
        return image.crs

    def image_mask_greater_than_0(self):
        mask = self.image_path.ReadAsArray() > 0
        plt.imshow(mask)
        plt.show(mask)
        return mask


if __name__ == '__main__':
    
    r = Raster("/media/dogosousa/56A22ED6A22EBA7F/BRUTA/CEBERS4/CBERS_4_MUX_20161205_148_113_L2/CBERS_4_MUX_20161205_148_113_L2.tif")

    src = r.read_image()
    print(src.get_crs())
    # plt.imshow(src)
    # plt.show(src)


        