import os
import fiona
import shutil
import UncompressFileAsEpsg4674 as u
import LandsatFileInfo as LcInfo
import Connection2Database as Conn
from shapely.geometry import shape, MultiPolygon


# TODO rever essa classe tendo em vista o descompressão das imagens em uma classe separada
class ComposeBands:

    def __init__(self, image_output_path, scene_image_name):
        # The folder where output processed will be saved
        self.image_output_path = image_output_path

        # Temporary folder to put files to process and remove after that
        self.tmp = u.UncompressFileAsEpsg4674.dir_tmp_img_epsg_4674

        self.file_name = scene_image_name

    def stack_all_30m_band_landsat(self):
        """
        Stacking all bands from landsat which has 30m spatial resolution.
        :return: File stacking with landsat bands from 1-7 and 9.
        """

        print('stack_all_30m_band_landsat...')

        command = "gdal_merge.py -separate -of HFA -co COMPRESSED=YES -o {tmp}{img_name}/ref.img " \
                  "{tmp}{img_name}/LC08*_B[1-7,9].TIF".format(tmp=self.tmp,
                                                              img_name=self.file_name())
        os.system(command)

    def stack_345_30m_band_landsat(self):
        """
        Stacking all bands usefull for forest monitor from landsat which has 30m spatial resolution. They are bands
        from 3 to 6
        :return: File stacking with landsat bands from 3-6.
        """
        print('stack_345_30m_band_landsat...')
        command = "gdal_merge.py -separate -of HFA -co COMPRESSED=YES -o {out}/{img_name}.TIF " \
                  "{tmp}{img_name}/LC08*_B[3-5].TIF".format(tmp=self.tmp,
                                                            out=self.image_output_path,
                                                            img_name=self.file_name())
        os.system(command)

    def stack_termal_band(self):
        """
        Stacking all thermal bands
        :return: File stacking with landsat bands from 0 and 1.
        """
        command = "gdal_merge.py -separate -of HFA -co COMPRESSED=YES -o {tmp}{img_name}/thermal.img " \
                  "{tmp}{img_name}/LC08*_B1[0,1].TIF".format(tmp=self.tmp,
                                                             img_name=self.file_name())
        os.system(command)

    def run_image_composition(self):
        """
        1) Create stacking from all image that have 30m of spatial resolution (size of pixel)
        2) Create stacking bands 345 from landsat image
        3) Create stacking bands from thermal landsat bands
        :return:
        """
        self.stack_all_30m_band_landsat()
        self.stack_345_30m_band_landsat()
        self.stack_termal_band()
