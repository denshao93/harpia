import os


class ClipRaster(object):

    def __init__(self, scene_image_name, dir_tmp_img):
        # Temporary folder to put files to process and remove after that
        self.dir_tmp_img = dir_tmp_img

        self.file_name = scene_image_name

        # Path where band files can be find.
        self.tmp_raw_img_path = os.path.join(self.dir_tmp_img, self.file_name)

        self.ref_img = os.path.join(self.dir_tmp_img, "ref.img")
        self.cut_img_vrt = os.path.join(self.dir_tmp_img, "cut_ref.vrt")
        self.cut_img_tif = os.path.join(self.dir_tmp_img, "cut_ref.tif")

    def clip_raster_by_mask(self):

        vector = "vetor/lc8_ba_4674_buffer.shp"

        command = "gdalwarp -cutline {vector} -crop_to_cutline -dstnodata 0 -multi " \
                  "{ref_img} {output_img}".format(vector=vector, ref_img=self.ref_img,
                                                output_img=self.cut_img_vrt)
        os.system(command)

    def compress_clieped_raster(self):

        command = "gdal_translate -ot Byte -scale -co compress=LZW -co NUM_THREADS=6 {cut_img_vrt} " \
        "{cut_img_tif}".format(cut_img_vrt=self.cut_img_vrt,
                                cut_img_tif=self.cut_img_tif)
        os.system(command)

    def del_img_vrt(self):
        os.remove(self.cut_img_vrt)

    def run(self):
        self.clip_raster_by_mask()
        self.compress_clieped_raster()
        self.del_img_vrt()
