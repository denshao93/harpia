import os
import Connection2Database as Con


class Segmentation:

    def __init__(self,
                 img_output_path_stored,
                 file_name):

        # The folder where output processed will be saved
        self.image_output_path = img_output_path_stored

        self.file_name = file_name

        self.img_output_path_stored = img_output_path_stored

        self.img_file_name_stored = '{}{}'.format(self.file_name,".TIF")

        # self.vector_file_name_stored = '{}{}'.format(self.file_name[:5],
        #                                         self.file_name[10:25])

        self.img_tif_path_stored = os.path.join(self.img_output_path_stored,
                                             self.img_file_name_stored)

    def get_segmentation(self, region, inter, algorithm):
        """Segmentation function by gdal-segment

        Arguments:
            region {int} -- [description]
            inter {int} -- Number of Interatiction
            algorithm {str} -- Kinds of segmentation which gdal-segment offers -
                               <LSC, SLICO, SLIC, SEEDS, MSLIC>
        """

        print("........Segmentanção.........")
        seg_output = os.path.join(self.image_output_path,
                                  self.file_name + "_" + algorithm + ".shp")
        command = "/home/diogocaribe/gdal-segment/bin/gdal-segment " \
                    "-region {r} " \
                    "-niter {i} " \
                    "-algo {algo} " \
                    "{input_img} " \
                    "-out {seg_output}".format(r=region,
                                                             i=inter,
                                                             algo=algorithm,
                                                             input_img=self.img_tif_path_stored,
                                                             seg_output=seg_output)
        os.system(command)

    def run_segmentation(self):
        """
        Segmenting landsat image
        :return:
        """
        self.get_segmentation(region=10, inter=25, algorithm="SLIC")
        # self.get_segmentation_lsc(10, 30)
        # self.get_segmentation_mslic(10, 10)
        # self.get_segmentation_slic(10, 10)
        # self.get_segmentation_seeds(10, 5)


if __name__ == "__main__":

    s = Segmentation(img_output_path_stored="/media/diogocaribe/56A22ED6A22EBA7F/PROCESSADA/" \
                                            "LC08/2017/12/215068/LC08_L1TP_215068_20171205_20171222_01_T1/",
                     file_name="LC08_215068_20171205")
    s.run_segmentation()

    # conn = Con.Connection("host=localhost dbname=ta7_rascunho user=postgres password=postgres")

    # # conn.create_scene_path_row_schema(satellite_name=,path_row="215068")
    # conn.load_segmentation_database(shapefile_path="~/Downloads/",
    #                                 shapefile_name="teste.shp")


