import os


class CloudShadow:

    def __init__(self):


    def create_angle_img(self):
        command = "fmask_usgsLandsatMakeAnglesImage.py -m {tmp}{img_name}*_MTL.txt -t {tmp}ref.img " \
                  "-o {tmp}angles.img" \
            .format(tmp=self.tmp, img_name=self.get_file_name_targz())
        os.system(command)

    def saturation_mask(self):
        command = "fmask_usgsLandsatSaturationMask.py -i {tmp}ref.img -m {tmp}{img_name}/*_MTL.txt " \
                  "-o {tmp}{img_name}/saturationmask.img" \
            .format(tmp=self.tmp, img_name=self.get_file_name_targz())
        os.system(command)

    def landsat_toa(self):
        command = "fmask_usgsLandsatTOA.py -i {tmp}{img_name}ref.img -m {tmp}{img_name}/*_MTL.txt " \
                  "-z {tmp}{img_name}/angles.img -o {tmp}{img_name}/toa.img" \
            .format(tmp=self.tmp, img_name=self.get_file_name_targz())
        os.system(command)

    def cloud_detection(self):
        command = "fmask_usgsLandsatStacked.py -t {tmp}{img_name}/thermal.img -a {tmp}{img_name}/toa.img " \
                  "-m {tmp}{img_name}/*_MTL.txt -z {tmp}{img_name}/angles.img " \
                  "-s {tmp}{img_name}/saturationmask.img -o {out}/{img_name}/cloud.img" \
            .format(tmp=self.tmp, out=self.image_output_path, img_name=self.get_file_name_targz())
        os.system(command)

    def cloud_raster2vector(self):
        command = "gdal_polygonize.py {out}cloud.img {out}cs_{file_name}.shp" \
            .format(out=self.get_folder_output_file_processed_path(), file_name=self.get_file_name_targz)
        os.system(command)


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
        # self.cloud_raster2vector()

