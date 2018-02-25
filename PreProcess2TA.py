import os
from glob import glob
import tarfile
import shutil
import LandsatFileInfo as lcinf


class PreProcess2TA:

    def __init__(self, raster_file_path_targz, set_output_processed_repo):
        # Input row file (landsat file compressed like dowloaded from USGS)
        self.raster_file_path_targz = raster_file_path_targz
        # OutputProcessed is a place where all processed output will be save (ex. compositions, segmentation)
        self.output_processed = set_output_processed_repo

        self.file_name = lcinf.LandsatFileInfo(self.raster_file_path_targz).get_file_name()
        # Temporary folder to put files to process and remove after that
        self.tmp_raster_folder = '{}{}{}'.format('/tmp/', self.file_name, '/')

    def create_folder_output_processed(self):
        """
        Creting folder to save all files processed from landsat raw files
        :return:
        """

        dir_list = glob('{}{}'.format(self.output_processed, "/*"), recursive=True)

        if '{}{}'.format(self.output_processed, 'PROCESSADA') not in dir_list:
            os.mkdir('{}{}'.format(self.output_processed, "/PROCESSADA"))

    def create_folder_output_file_processed(self):

        dir_list = glob('{}{}'.format(self.output_processed, "/*/*"), recursive=True)
        raster_output_processed_files = '{}{}{}'.format(self.output_processed, 'PROCESSADA/', self.file_name)

        if raster_output_processed_files not in dir_list:
            os.mkdir(raster_output_processed_files)

    def get_folder_output_file_processed(self):

        return '{}{}{}{}'.format(self.output_processed, 'PROCESSADA/', self.file_name, '/')

    def uncompress_targz(self):

        tar = tarfile.open(self.raster_file_path_targz, "r")
        tar.extractall('/tmp')
        tar.close()

    def stack_all_30m_band(self):
        """
        Stacking all bands from landsat which has 30m spatial resolution.
        :return: File stacking with landsat bands from 1-7 and 9.
        """

        command = "gdal_merge.py -separate -of HFA -co COMPRESSED=YES -o {tmp}ref.img " \
                  "{tmp}LC08*_B[1-7,9].TIF".format(tmp=self.tmp_raster_folder)
        os.system(command)

    def stack_345_30m_band(self):
        """
        Stacking all bands usefull for forest monitor from landsat which has 30m spatial resolution. They are bands
        from 3 to 6
        :return: File stacking with landsat bands from 3-6.
        """
        command = "gdal_merge.py -separate -of HFA -co COMPRESSED=YES -o {out}{file_name}.TIF " \
                  "{tmp}LC08*_B[3-5].TIF".format(tmp=self.tmp_raster_folder,
                                                 out=self.get_folder_output_file_processed(),
                                                 file_name=self.file_name)
        os.system(command)

    def stack_termal_band(self):
        """
        Stacking all thermal bands
        :return: File stacking with landsat bands from 0 and 1.
        """
        command = "gdal_merge.py -separate -of HFA -co COMPRESSED=YES -o {tmp}thermal.img " \
                  "{tmp}LC08*_B1[0,1].TIF".format(tmp=self.tmp_raster_folder)
        os.system(command)

    def create_angle_img(self):

        command = "fmask_usgsLandsatMakeAnglesImage.py -m {tmp}*_MTL.txt -t {tmp}ref.img -o {tmp}angles.img"\
            .format(tmp=self.tmp_raster_folder)
        os.system(command)

    def saturation_mask(self):

        command = "fmask_usgsLandsatSaturationMask.py -i {tmp}ref.img -m {tmp}*_MTL.txt -o {tmp}saturationmask.img"\
            .format(tmp=self.tmp_raster_folder)
        os.system(command)

    def landsat_toa(self):

        command = "fmask_usgsLandsatTOA.py -i {tmp}ref.img -m {tmp}*_MTL.txt -z {tmp}angles.img -o {tmp}toa.img"\
            .format(tmp=self.tmp_raster_folder)
        os.system(command)

    def cloud_detection(self):

        command = "fmask_usgsLandsatStacked.py -t {tmp}thermal.img -a {tmp}toa.img -m {tmp}*_MTL.txt -z " \
                  "{tmp}angles.img -s {tmp}saturationmask.img -o {out}cloud.img"\
            .format(tmp=self.tmp_raster_folder, out=self.get_folder_output_file_processed())
        os.system(command)

    def cloud_raster2vector(self):

        command = "gdal_polygonize.py {out}cloud.img {out}cs_{file_name}.shp"\
            .format(out=self.get_folder_output_file_processed(), file_name=self.file_name)
        os.system(command)

    def del_folder_file_tmp(self):

        shutil.rmtree(self.tmp_raster_folder)

    def get_segmentation_slico(self, region, inter):
        """
        Slico is a kind of algorith to segmentation
        The object created is great compactness
        :return:
        """
        command = "~/gdal-segment/bin/gdal-segment -algo LSC -region {r} -niter {i} {tmp}ref.img -out {out}" \
                  "{file_name}-slico.shp".format(r=region,
                                                 i=inter,
                                                 tmp=self.tmp_raster_folder,
                                                 out=self.get_folder_output_file_processed(),
                                                 file_name=self.file_name)
        os.system(command)

    def get_segmentation_seeds(self, region, inter):
        """
        Seeds is a kind of algorith to segmentation
        :return:
        """
        command = "~/gdal-segment/bin/gdal-segment -algo SEEDS -region {r} -niter {i} {out}{file_name}.TIF -out " \
                  "{out}{file_name}-seeds.shp".format(r=region,
                                                      i=inter,
                                                      tmp=self.tmp_raster_folder,
                                                      out=self.get_folder_output_file_processed(),
                                                      file_name=self.file_name)
        os.system(command)

    def run_cloud_shadow_fmask(self):

        self.create_folder_output_processed()
        self.create_folder_output_file_processed()
        self.uncompress_targz()
        self.stack_all_30m_band()
        self.stack_345_30m_band()
        self.stack_termal_band()
        self.create_angle_img()
        self.saturation_mask()
        self.landsat_toa()
        self.cloud_detection()
        self.cloud_raster2vector()

    def run_segmentation(self):

        self.get_segmentation_slico(10, 10)
        # self.get_segmentation_seeds(8, 25)