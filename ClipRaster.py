import os


class ClipRaster(object):

    def __init__(self):


    def check_if_clip(self, satellite_index, aoi_project):
        """Verify if image have to be cliped.

        Argument:
            satellite_index (geom) -- [description]
            aoi_project (geom) -- [description]
        """

        pass
    def clip_raster_by_mask(self):

        print("........Clip raster........")
        vector = os.path.join(self.dir_tmp_img, "intersect_pathrow_ba.shp")

        command =   "gdalwarp -t_srs EPSG:4674 -cutline {vector} -crop_to_cutline -multi " \
                    "{ref_img} {output_img}".format(vector=vector, ref_img=self.ref_img,
                                                    output_img=self.cut_img_vrt)
        os.system(command)

    def compress_cliped_raster(self):

        print("........Compress raster........")
        command =   "gdal_translate -ot Byte -scale -co compress=LZW -b 3 -b 2 -b 1 {cut_img_vrt} " \
                    "{cut_img_tif}".format( cut_img_vrt=self.cut_img_vrt,
                                            cut_img_tif=self.cut_img_tif_path)

        os.system(command)

    def del_img_vrt(self):
        os.remove(self.cut_img_vrt)

    def run(self):
        self.clip_raster_by_mask()
        self.compress_cliped_raster()
        self.del_img_vrt()
