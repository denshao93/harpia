import os


class ClipRaster(object):

    def __init__(self, scene_image_name, dir_tmp_img, img_output_path_stored, img_file_name_stored):
        # Temporary folder to put files to process and remove after that
        self.dir_tmp_img = dir_tmp_img

        self.file_name = scene_image_name

        self.img_output_path_stored = img_output_path_stored

        # Path where band files can be find.
        self.tmp_raw_img_path = os.path.join(self.dir_tmp_img, self.file_name)

        self.ref_img = os.path.join(self.dir_tmp_img, self.file_name+".TIF")
        self.cut_img_vrt = os.path.join(self.dir_tmp_img, "cut_ref.vrt")

        self.file_name_stored = '{}{}'.format(img_file_name_stored, ".TIF")

        self.cut_img_tif_path = os.path.join(self.img_output_path_stored,
                                             self.file_name_stored)

    def clip_raster_by_mask(self):

        vector = "vetor/lc8_ba_32624.shp"

        command = "gdalwarp -cutline {vector} -crop_to_cutline -multi " \
                  "{ref_img} {output_img}".format(vector=vector, ref_img=self.ref_img,
                                                output_img=self.cut_img_vrt)
        os.system(command)

    def compress_clieped_raster(self):

        command = "gdal_translate -ot Byte -scale -co compress=LZW -co NUM_THREADS=6 {cut_img_vrt} " \
        "{cut_img_tif}".format(cut_img_vrt=self.cut_img_vrt,
                                cut_img_tif=self.cut_img_tif_path)
        os.system(command)

    def del_img_vrt(self):
        os.remove(self.cut_img_vrt)

    def run(self):
        self.clip_raster_by_mask()
        self.compress_clieped_raster()
        self.del_img_vrt()
