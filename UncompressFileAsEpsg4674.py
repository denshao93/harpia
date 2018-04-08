import os
import sys
import shutil
import tarfile
import tempfile
from glob import glob


class UncompressFileAsEpsg4674:

    def __init__(self, image_file_path_targz):

        # Input row file (landsat file compressed like dowloaded from USGS)
        self.image_file_path_targz = image_file_path_targz

        # Temporary folder to put files to process and remove after that
        self.tmp = tempfile.gettempdir()

        # Tmp directory useful to convert landsat imagens from UTM N to Sirgas2000
        self.dir_tmp_img_utm_north = tempfile.mkdtemp(prefix='raw_')
        self.dir_tmp_img_epsg_4674 = tempfile.mkdtemp(prefix='reprojected_')

    # def dir_tmp_img_epsg_4674(self):
    #
    #     return tempfile.mkdtemp()

    @staticmethod
    def get_file_basename(file_path):

        basename = os.path.basename(file_path)

        file_name = basename.split('.')[0]

        return file_name

    @staticmethod
    def get_file_name_extension(file_path):

        file_name_extension = os.path.basename(file_path)

        return file_name_extension

    def uncompress_img_raw_utm_north(self):
        """
        This function uncompress tar.gz files donwloaded from USGS
        :return:
        """
        with tarfile.open(self.image_file_path_targz, "r") as tar:
            tar.extractall(self.dir_tmp_img_utm_north)

    def copy_metadata_file_from_landsat8(self):

        txt_file = glob('{}{}'.format(self.dir_tmp_img_utm_north,"/*/*.txt"))

        for file_path in txt_file:
            file_name_extension = self.get_file_name_extension(file_path)
            shutil.copyfile(src=file_path,
                            dst=os.path.join(self.dir_tmp_img_epsg_4674, file_name_extension))

    def reproject_img_from_umt_north_to_sirgas2000(self):

        list_raster_folder = glob('{}{}'.format(self.dir_tmp_img_utm_north, '/*/*TIF'))

        for tif in list_raster_folder:
            img_name = tif.split('/')[-1]
            command = "gdalwarp {img_src} {img_output}/{img_name} -s_srs EPSG:32624 -t_srs EPSG:4674" \
                .format(img_src=tif,
                        img_output=self.dir_tmp_img_epsg_4674,
                        img_name=img_name)
            os.system(command)

    @staticmethod
    def close_tmp_dir(dir):
        shutil.rmtree(dir)

    def run(self):
        self.uncompress_img_raw_utm_north()
        self.copy_metadata_file_from_landsat8()
        self.reproject_img_from_umt_north_to_sirgas2000()
        # self.close_tmp_dir(self.dir_tmp_img_utm_north)


if __name__ == "__main__":

    unsirgas = UncompressFileAsEpsg4674(image_file_path_targz=sys.argv[1])

    unsirgas.run()




