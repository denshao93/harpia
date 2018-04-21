import rasterio
import gdal
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
    
    r = Raster("/home/dogosousa/Downloads/LC08_L1TP_215068_20171205_20171222_01_T1/LC08_L1TP_215068_20171205_20171222_01_T1_B1.TIF")

    src = r.read_image()
    
    plt.imshow(src)
    plt.show(src)


        