import os
import fiona
import shutil
import tarfile
import tempfile
from glob import glob
import LandsatFileInfo as LCinf
import ConnectionTaDatabase as Conn
from shapely.geometry import shape, MultiPolygon


class PreProcess2TA:

    def __init__(self, raster_file_path_targz, set_output_processed_repo):
        # Input row file (landsat file compressed like dowloaded from USGS)
        self.raster_file_path_targz = raster_file_path_targz
        # OutputProcessed is a place where all processed output will be save (ex. compositions, segmentation)
        self.output_processed = set_output_processed_repo

        self.file_name_targz = LCinf.LandsatFileInfo(self.raster_file_path_targz).get_file_name()
        # Temporary folder to put files to process and remove after that
        # self.tmp_raster_folder = '{}{}{}'.format('/tmp/', self.file_name_targz, '/')
        self.tmp = tempfile.gettempdir()

    def create_folder_output_processed(self):
        """
        Creting folder to save all scenes processed from landsat raw files (results from processing)
        :return: Folder called as "PROCESSADA"
        """

        dir_list = glob('{}{}'.format(self.output_processed, "/*"), recursive=True)

        if '{}{}'.format(self.output_processed, 'PROCESSADA') not in dir_list:
            os.mkdir('{}{}'.format(self.output_processed, "/PROCESSADA"))

    def get_folder_output_processed_path(self):

        return '{}{}'.format(self.output_processed, 'PROCESSADA')

    def create_folder_output_file_processed(self):

        dir_list = glob('{}{}'.format(self.output_processed, "/*/*"), recursive=True)
        raster_output_processed_files = '{}{}{}'.format(self.output_processed, 'PROCESSADA/', self.file_name_targz)

        if raster_output_processed_files not in dir_list:
            os.mkdir(raster_output_processed_files)

    def get_folder_output_file_processed_path(self):

        return '{}{}{}{}'.format(self.output_processed, 'PROCESSADA/', self.file_name_targz, '/')

    def get_folder_tmp_scene_name(self):

        return '{}{}{}'.format(self.tmp, self.file_name_targz, '/')

    def uncompress_targz_image_as_epsg_4674(self):
        """
        This function uncompress tar.gz files donwloaded from USGS
        Befeor it, all image files are converted from WGS 84 UTM 24N to SIRGAS 2000
        :return:
        """

        try:
            tmp = tempfile.mkdtemp()
            output_folder_reprojetcted = '{}/{}'.format(self.tmp, self.file_name_targz)

            if not os.path.exists(output_folder_reprojetcted):
                os.mkdir('{}/{}'.format(self.tmp, self.file_name_targz))

            with tarfile.open(self.raster_file_path_targz, "r") as tar:
                tar.extractall('{}/'.format(tmp))

            list_raster_folder = glob('{}{}'.format(tmp, '/*/*TIF'))

            for tif in list_raster_folder:
                img_name = tif.split('/')[-1]
                command = "gdalwarp {img_src} {img_output}/{img_name}.TIF -s_srs EPSG:32624 -t_srs EPSG:4674" \
                    .format(img_src=tif,
                            img_output=output_folder_reprojetcted,
                            img_name=img_name)
                os.system(command)

        except IOError:
            print('IOError')
        finally:
            shutil.rmtree(tmp)

    def stack_all_30m_band_landsat(self):
        """
        Stacking all bands from landsat which has 30m spatial resolution.
        :return: File stacking with landsat bands from 1-7 and 9.
        """

        command = "gdal_merge.py -separate -of HFA -co COMPRESSED=YES -o {tmp}ref.img " \
                  "{tmp}LC08*_B[1-7,9].TIF".format(tmp=self.tmp)
        os.system(command)

    def stack_345_30m_band_landsat(self):
        """
        Stacking all bands usefull for forest monitor from landsat which has 30m spatial resolution. They are bands
        from 3 to 6
        :return: File stacking with landsat bands from 3-6.
        """
        command = "gdal_merge.py -separate -of HFA -co COMPRESSED=YES -o {out}{file_name}.TIF " \
                  "{tmp}LC08*_B[3-5].TIF".format(tmp=self.tmp,
                                                 out=self.get_folder_output_file_processed_path(),
                                                 file_name=self.file_name_targz)
        os.system(command)

    def stack_termal_band(self):
        """
        Stacking all thermal bands
        :return: File stacking with landsat bands from 0 and 1.
        """
        command = "gdal_merge.py -separate -of HFA -co COMPRESSED=YES -o {tmp}thermal.img " \
                  "{tmp}LC08*_B1[0,1].TIF".format(tmp=self.tmp)
        os.system(command)

    def create_angle_img(self):

        command = "fmask_usgsLandsatMakeAnglesImage.py -m {tmp}*_MTL.txt -t {tmp}ref.img -o {tmp}angles.img"\
            .format(tmp=self.tmp)
        os.system(command)

    def saturation_mask(self):

        command = "fmask_usgsLandsatSaturationMask.py -i {tmp}ref.img -m {tmp}*_MTL.txt -o {tmp}saturationmask.img"\
            .format(tmp=self.tmp)
        os.system(command)

    def landsat_toa(self):

        command = "fmask_usgsLandsatTOA.py -i {tmp}ref.img -m {tmp}*_MTL.txt -z {tmp}angles.img -o {tmp}toa.img"\
            .format(tmp=self.tmp)
        os.system(command)

    def cloud_detection(self):

        command = "fmask_usgsLandsatStacked.py -t {tmp}thermal.img -a {tmp}toa.img -m {tmp}*_MTL.txt -z " \
                  "{tmp}angles.img -s {tmp}saturationmask.img -o {out}cloud.img"\
            .format(tmp=self.tmp, out=self.get_folder_output_file_processed_path())
        os.system(command)

    def cloud_raster2vector(self):

        command = "gdal_polygonize.py {out}cloud.img {out}cs_{file_name}.shp"\
            .format(out=self.get_folder_output_file_processed_path(), file_name=self.file_name_targz)
        os.system(command)

    def del_folder_file_tmp(self):

        shutil.rmtree(self.tmp)

    def get_segmentation_slico(self, region, inter):
        """
        Slico is a kind of algorith to segmentation
        The object created is great compactness
        :return:
        """
        command = "~/gdal-segment/bin/gdal-segment -algo LSC -region {r} -niter {i} {tmp}ref.img -out {out}" \
                  "{file_name}-slico.shp".format(r=region,
                                                 i=inter,
                                                 tmp=self.tmp,
                                                 out=self.get_folder_output_file_processed_path(),
                                                 file_name=self.file_name_targz)
        os.system(command)

    def get_segmentation_seeds(self, region, inter):
        """
        Seeds is a kind of algorith to segmentation
        :return:
        """
        command = "~/gdal-segment/bin/gdal-segment -algo SEEDS -region {r} -niter {i} {out}{file_name}.TIF -out " \
                  "{out}{file_name}-seeds.shp".format(r=region,
                                                      i=inter,
                                                      tmp=self.tmp,
                                                      out=self.get_folder_output_file_processed_path(),
                                                      file_name=self.file_name_targz)
        os.system(command)

    def get_geom_from_lc_ba_scene(self):

        connection = Conn.Connection("host=localhost dbname=ta7 user=postgres password=postgres")
        pathrow = LCinf.LandsatFileInfo(self.raster_file_path_targz).get_path_row_from_file()
        path_row = '{}/{}'.format(pathrow[0], pathrow[1])
        lc_scene_geom = connection.get_scene_path_row_geom(path_row)[0][2]

        return lc_scene_geom

    def read_segmentation_shp(self):
        """
        Reading segmentation results from output folder
        :return: Segments from segmentation that intersect landsat scene interested to Bahia monitoring forest project
        """
        file_path = '{out}{file_name}-seeds.shp'.format(out=self.get_folder_output_file_processed_path(),
                                                        file_name=self.file_name_targz)
        # MultiPolygon from the list of Polygons
        multipoly = MultiPolygon([shape(pol['geometry']) for pol in fiona.open(file_path)])

        return multipoly

    def run_make_folder_input_data(self):
        """
        1) Create folder where all scene of landsat images will be saved
        2) Create folder where files from only one landsat scene images will be saved (results of one scene)
        3) Uncompress tar.gz file and save all bands of landsat in tmp folder
        4) Create stacking from all image that have 30m of spatial resolution (size of pixel)
        5) Create stacking bands 345 from landsat image
        6) Create stacking bands from thermal landsat bands
        :return:
        """
        # self.create_folder_output_processed()
        # self.create_folder_output_file_processed()
        self.uncompress_targz_image_as_epsg_4674()
        # self.stack_all_30m_band_landsat()
        # self.stack_345_30m_band_landsat()
        # self.stack_termal_band()
        # self.reproject_raster_from_folder()

    def run_cloud_shadow_fmask(self):
        """
        Run fsmak that will return classification of image processed which have five classes (cloud, shadow, water,
         "soil")
        The output will be raster and vectorda
        :return:
        """

        self.create_angle_img()
        self.saturation_mask()
        self.landsat_toa()
        self.cloud_detection()
        self.cloud_raster2vector()

    def run_segmentation(self):
        """
        Segmenting landsat image
        :return:
        """

        # self.get_segmentation_slico(10, 10)
        # self.get_segmentation_seeds(8, 25)
        pass

