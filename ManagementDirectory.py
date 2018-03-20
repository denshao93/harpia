import sys
from glob import glob


class ManagementDirectory:

    def __init__(self,
                 dir_all_targz,
                 raster_file_path_targz,
                 output_dir_image_processed):
        """
        This class organizes folder in order to have structure directories to pre-processing landsast images
        :param dir_all_targz: Directory that store all tar.gz files downloaded from USGS.
        :param raster_file_path_targz: Path of tar.gz file stored in directory
        :param output_dir_image_processed: The root directory where image processed will be stored organized
                                           by name of satellite, year and path row (ex.from landsat 8:
                                           LC8/2017/215069).
        """
        # Input row file (landsat file compressed (tar.gz) downloaded from USGS).
        self.raster_file_path_targz = raster_file_path_targz

        # Root directory where all landsat image downloaded were stored.
        self.dir_all_targz = dir_all_targz

        # Output image processed is a place where image processed output will be stored (ex. compositions, segmentation)
        self.output_dir_image_processed = output_dir_image_processed

    def create_root_dir_processed(self, name_of_folder):
        """
        :param name_of_folder: Given directory name where all scene processed will be organized and stored
        :return:
        """

        pass

    def get_list_targz_files_from_dir_all_targz(self):
        """
        Getting list of tar.gz files in folders recursively
        :return: list of tar.gz files
        """
        return glob('{}{}'.format(self.dir_all_targz, '/*tar.gz'), recursive=True)


    def get_folder_name():

        return glob(folder, recursive=True)


    def get_list_folder_name_from_processed_dir(folder):

        list_folder = glob('{}{}'.format(folder, '/*/'))
        list_folder_name = [i.split('/')[-2] for i in [i.split(',')[0] for i in list_folder]]
        return list_folder_name


if __name__ == "__main__":

    mdir = ManagementDirectory(dir_all_targz=sys.argv[1],
                               raster_file_path_targz=sys.argv[2],
                               output_dir_image_processed=sys.argv[3])
    mdir.dir_all_targz





