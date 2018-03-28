import os
import UncompressFileAsEpsg4674 as u


class Segmentation:

    def __init__(self, image_output_path, file_name):
        # The folder where output processed will be saved
        self.image_output_path = image_output_path

        # Temporary folder to put files to process and remove after that
        self.tmp = u.UncompressFileAsEpsg4674.dir_tmp_img_epsg_4674

        self.file_name = file_name

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
                                                 file_name=self.get_file_name_targz)
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
                                                      file_name=self.get_file_name_targz)
        os.system(command)

    def run_segmentation(self):
        """
        Segmenting landsat image
        :return:
        """

        self.get_segmentation_slico(10, 10)
        # self.get_segmentation_seeds(8, 25)