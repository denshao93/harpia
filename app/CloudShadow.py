import os


class CloudShadow:

    def __init__(self,
                 dir_tmp_img,
                 image_output_path,
                 file_name):

        self.file_name = file_name

        self.tmp = dir_tmp_img

        self.image_output_path = image_output_path

    def create_angle_img(self):
        print(".....Creating angle image....")
        command = "fmask_usgsLandsatMakeAnglesImage.py -m {tmp}/{file_name}/*_MTL.txt -t {tmp}/ref.img " \
                  "-o {tmp}/angles.img".format(tmp=self.tmp, file_name=self.file_name)
        os.system(command)

    def saturation_mask(self):
        print(".....Creating saturation image....")
        command = "fmask_usgsLandsatSaturationMask.py -i {tmp}/ref.img -m {tmp}/{file_name}/*_MTL.txt" \
                  " -o {tmp}/saturationmask.img".format(tmp=self.tmp, file_name=self.file_name)
        os.system(command)

    def landsat_toa(self):
        print(".....Creating TOA image....")
        command = "fmask_usgsLandsatTOA.py -i {tmp}/ref.img -m {tmp}/{file_name}/*_MTL.txt -z {tmp}/angles.img " \
                  "-o {tmp}/toa.img".format(tmp=self.tmp, file_name=self.file_name)
        os.system(command)

    def cloud_detection(self):
        print(".....Creating cloud detection image....")
        command = "fmask_usgsLandsatStacked.py -t {tmp}/thermal.img -a {tmp}/toa.img -m {tmp}/{file_name}/*_MTL.txt " \
                  "-z {tmp}/angles.img -s {tmp}/saturationmask.img -o {out}/cloud.tif" \
            .format(tmp=self.tmp, out=self.image_output_path, file_name=self.file_name)
        os.system(command)

    def cloud_raster2vector(self):
        command = "gdal_polygonize.py {out}cloud.img {out}cs_{file_name}.shp" \
            .format(out=self.image_output_path, file_name=self.file_name)
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
