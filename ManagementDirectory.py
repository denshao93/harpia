import os
import sys
import tempfile as tmp


class ManagementDirectory:

    def __init__(self,
                 dir_all_targz,
                 raster_file_path_targz,
                 output_root_dir_image_processed):
        """
        This class organizes folder in order to have structure directories to pre-processing landsast images
        :param dir_all_targz: Directory that store all tar.gz files downloaded from USGS.
        :param raster_file_path_targz: Path of tar.gz file stored in directory
        :param output_root_dir_image_processed: The root directory where image processed will be stored organized
                                           by name of satellite, year and path row (ex.from landsat 8:
                                           LC8/2017/215069).
        """
        # Input row file (landsat file compressed (tar.gz) downloaded from USGS).
        self.raster_file_path_targz = raster_file_path_targz

        # Root directory where all landsat image downloaded were stored.
        self.dir_all_targz = dir_all_targz

        # Output image processed is a place where image processed output will be stored (ex. compositions, segmentation)
        self.output_dir_image_processed = output_root_dir_image_processed

    def create_root_dir_processed(self, dir_name):
        """
        Creating directory where files will be organized. This is the processed directory ooutput.
        The sugestion is that set name as PROCESSADA
        :param dir_name: Giving name for directory where all scene processed will be organized and stored
        :return:
        """
        dir_path = '{}/{}'.format(self.output_dir_image_processed, dir_name)

        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

    def get_file_name_from_targz(self):

        return os.path.basename(self.raster_file_path_targz)

    def get_path_row_from_targz(self):

        return self.get_file_name_from_targz()[10:15]

    # TODO fazendo a criação da pasta com year/pathrow/namefile.tar.gz
    def create_image_year_pathrow_dir(self):

        dir_path = '{}/{}'.format(self.output_dir_image_processed)

        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

    def create_tmp_folder(self):

        temp = tmp.TemporaryDirectory()

        return temp

    def close_tmp_folder(self):

        self.create_tmp_folder().cleanup()

    def get_tmp_folder_path(self):

        self.create_tmp_folder()

    def run_manage_directory(self):

        # Making folder which will store files processed
        self.create_root_dir_processed('PROCESSADA')
        self.create_image_year_pathrow_dir()

        # Creating tmp folder to put row image bands used to processed
        self.create_tmp_folder()





if __name__ == "__main__":

    mdir = ManagementDirectory(dir_all_targz=sys.argv[1],
                               raster_file_path_targz=sys.argv[2],
                               output_root_dir_image_processed=sys.argv[3])







