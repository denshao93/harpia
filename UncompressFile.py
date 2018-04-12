import os
import shutil
import tarfile
import tempfile
from glob import glob


class UncompressFile:

    def __init__(self, image_file_path_targz):

        # Input row file (landsat file compressed like dowloaded from USGS)
        self.image_file_path_targz = image_file_path_targz

        # Temporary folder to put files to process and remove after that
        self.tmp = tempfile.gettempdir()

        # Tmp directory useful to convert landsat imagens from UTM N to Sirgas2000
        self.dir_tmp_img = tempfile.mkdtemp()

    @staticmethod
    def get_file_basename(file_path):

        basename = os.path.basename(file_path)

        file_name = basename.split('.')[0]

        return file_name

    @staticmethod
    def get_file_name_extension(file_path):

        file_name_extension = os.path.basename(file_path)

        return file_name_extension

    def uncompress_img(self):
        """
        This function uncompress tar.gz files donwloaded from USGS
        :return:
        """
        with tarfile.open(self.image_file_path_targz, "r") as tar:
            tar.extractall(self.dir_tmp_img)

    def reproject_img_from_umt_north_to_sirgas2000(self):

        list_raster_folder = glob('{}{}'.format(self.dir_tmp_img, '/*/*TIF'))

        for tif in list_raster_folder:
            img_name = tif.split('/')[-1]
            command = "gdalwarp {img_src} {img_output}/{img_name} -s_srs EPSG:32624 -t_srs EPSG:4674" \
                .format(img_src=tif,
                        img_output=self.dir_tmp_img_epsg_4674,
                        img_name=img_name)
            os.system(command)

    @staticmethod
    def close_tmp_dir(dir_path):
        shutil.rmtree(dir_path)

    def run(self):
        self.uncompress_img()
        # self.reproject_img_from_umt_north_to_sirgas2000()
        # self.close_tmp_dir(self.dir_tmp_img_utm_north)



