import os
import Connection2Database as Con


class Segmentation:

    def __init__(self,
                 image_output_path,
                 dir_tmp_image,
                 file_name):

        # The folder where output processed will be saved
        self.image_output_path = image_output_path

        # Temporary folder to put files to process and remove after that
        self.dir_tmp_image = dir_tmp_image

        self.file_name = file_name

    def get_segmentation_slic(self, region, inter):
        """
        Slic is a kind of algorith to segmentation
        Very good to separate object from
        :return:
        """
        print("........Segmentanção.........")
        command = "/home/diogocaribe/src/gdal-segment/bin/gdal-segment -algo SLIC -region {r} -niter {i} {tmp}{file_name}.TIF " \
                  "-out {out}/{file_name}-slic.shp".format(r=region,
                                                            i=inter,
                                                            tmp=self.dir_tmp_image,
                                                            out=self.image_output_path,
                                                            file_name=self.file_name)
        os.system(command)

    def get_segmentation_lsc(self, region, inter):
        """
        Slic is a kind of algorith to segmentation
        Very good to separate object from
        :return:
        """
        print("........Segmentanção.........")
        command = "~/src/gdal-segment/bin/gdal-segment -algo LSC -region {r} -niter {i} {tmp}{file_name}.TIF " \
                  "-out {out}/{file_name}-lsc.shp".format(r=region,
                                                            i=inter,
                                                            tmp=self.dir_tmp_image,
                                                            out=self.image_output_path,
                                                            file_name=self.file_name)
        os.system(command)

    def get_segmentation_mslic(self, region, inter):
        """
        Slic is a kind of algorith to segmentation
        Very good to separate object from
        :return:
        """
        print("........Segmentanção.........")
        command = "~/src/gdal-segment/bin/gdal-segment -algo MSLIC -region {r} -niter {i} {tmp}{file_name}.tif " \
                  "-out {out}/{file_name}-mslic.shp".format(r=region,
                                                            i=inter,
                                                            tmp=self.dir_tmp_image,
                                                            out=self.image_output_path,
                                                            file_name=self.file_name)
        os.system(command)

    def get_segmentation_seeds(self, region, inter):
        """
        Seeds is a kind of algorith to segmentation
        The image have to have 3 bands or gray with
        :return:
        """
        command = "~/src/gdal-segment/bin/gdal-segment -algo SEEDS -region {r} -niter {i} {out}/{file_name}.tif -out " \
                  "{out}/{file_name}-seeds.shp".format(r=region,
                                                       i=inter,
                                                       tmp=self.dir_tmp_image,
                                                       out=self.image_output_path,
                                                       file_name=self.file_name)
        os.system(command)

    def run_segmentation(self):
        """
        Segmenting landsat image
        :return:
        """
        # self.get_segmentation_lsc(10, 30)
        # self.get_segmentation_mslic(10, 10)
        self.get_segmentation_slic(8, 2)
        # self.get_segmentation_seeds(10, 5)


if __name__ == "__main__":

    s = Segmentation(image_output_path="/tmp/tmpz__mgdje/",
                     dir_tmp_image="/tmp/tmpz__mgdje/",
                     file_name="cut_ref")
    s.run_segmentation()

    # conn = Con.Connection("host=localhost dbname=ta7_rascunho user=postgres password=postgres")

    # # conn.create_scene_path_row_schema(satellite_name=,path_row="215068")
    # conn.load_segmentation_database(shapefile_path="~/Downloads/",
    #                                 shapefile_name="teste.shp")


