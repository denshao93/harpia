import os
import Raster as R
import geo_utils as gu
from shapely import wkt


class ClipRaster:

    def __init__(self, img_path):
        self.image_path = img_path

    def check_img_will_be_cliped(self):
        """Verify if image have to be cliped.

        If img overlap boundery of area of interested project (aoi),
        It should be cliped to remove image that not be useless.

        Argument:
            satellite_index (geom) -- [description]
            aoi_project (geom) -- [description]
        """
        ba_line = gu.read_shapefile_poly("/home/diogocaribe/workspace/harpia/vector/ba_4674_line.shp")
        trace_outline = R.Raster(self.image_path).trace_outline_from_raster_wkt()
        trace_outline = wkt.loads(trace_outline)

        check_intersects = trace_outline.intersects(ba_line)

        return check_intersects

    # def clip_raster_by_mask(self):

    #     print("........Clip raster........")
    #     vector = os.path.join(self.dir_tmp_img, "intersect_pathrow_ba.shp")

    #     command =   "gdalwarp -t_srs EPSG:4674 -cutline {vector} -crop_to_cutline -multi " \
    #                 "{ref_img} {output_img}".format(vector=vector, ref_img=self.ref_img,
    #                                                 output_img=self.cut_img_vrt)
    #     os.system(command)

    # def compress_cliped_raster(self):

    #     print("........Compress raster........")
    #     command =   "gdal_translate -ot Byte -scale -co compress=LZW -b 3 -b 2 -b 1 {cut_img_vrt} " \
    #                 "{cut_img_tif}".format( cut_img_vrt=self.cut_img_vrt,
    #                                         cut_img_tif=self.cut_img_tif_path)

    #     os.system(command)

    # def del_img_vrt(self):
    #     os.remove(self.cut_img_vrt)

    # def run(self):
    #     self.clip_raster_by_mask()
    #     self.compress_cliped_raster()
    #     self.del_img_vrt()

if __name__ == "__main__":

    ClipRaster(img_path=f"/tmp/tmp2qtqk6i6/" \
                        f"LC08_L1TP_215068_20171205_20171222_01_T1.TIF")\
                        .check_img_will_be_cliped()