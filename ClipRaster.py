class ClipRaster(object):

    def clip_raster_by_mask(self):

        vector = "vetor/square_215068.shp"
        command = "gdalwarp -cutline {vector} -crop_to_cutline -dstnodata 0 -multi "\
                  "{tmp}/ref.img {tmp}/cut_ref.vrt".format(vector=vector,
                                                                       tmp=self.dir_tmp_img,
                                                                       file_name=self.file_name)
        os.system(command)

    def compress_clieped_raster(self):

        command = "gdal_translate -ot Byte -scale -co compress=LZW -co NUM_THREADS=6 {tmp}/cut_ref.vrt " \
        "{tmp}/cut_ref.tif".format(tmp=self.dir_tmp_img,
                                   file_name=self.file_name)
        os.system(command)