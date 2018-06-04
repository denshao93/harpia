import rasterio
import geo_utils as gu


class Raster:

    def __init__(self, image_path):

        self.image_path = image_path

    def read_image(self):

        image = rasterio.open(self.image_path)

        return image

    def get_espg_image(self):

        image = rasterio.open(self.image_path)

        return image.crs

    def bounds_raster(self):

        return self.read_image().bounds

    def bounds_raster_polygon(self):

        poly = gu.create_polygon_from_bbox_1(self.bounds_raster())

        return poly

if __name__ == '__main__':

    r = Raster("/home/diogocaribe/Documents/LC08_L1TP_215068_20171205_20171222_01_T1/LC08_L1TP_215068_20171205_20171222_01_T1_B1.TIF")

    src = r.read_image()
    r.bounds_raster_polygon()