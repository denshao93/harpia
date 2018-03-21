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
        self.output_root_dir_image_processed = output_root_dir_image_processed

    def create_root_dir_processed(self, dir_name):
        """
        Creating directory where files will be organized. This is the processed directory ooutput.
        The sugestion is that set name as PROCESSADA
        :param dir_name: Giving name for directory where all scene processed will be organized and stored
        :return:
        """
        dir_path = '{}/{}'.format(self.output_root_dir_image_processed, dir_name)

        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

    def get_file_name_from_targz(self):

        base = os.path.basename(self.raster_file_path_targz)

        return '.'.join(base.split('.')[:-2])

    def get_path_row_from_targz(self):

        return self.get_file_name_from_targz()[10:16]

    def get_image_year_aquisition_date(self):

        return self.get_file_name_from_targz()[17:21]

    def create_image_year_pathrow_dir(self):

        dir_path = '{}/PROCESSADA/{year}/' \
                   '{path_row}/{file_name}/'.format(self.output_root_dir_image_processed,
                                                    year=self.get_image_year_aquisition_date(),
                                                    path_row=self.get_path_row_from_targz(),
                                                    file_name=self.get_file_name_from_targz())

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def run_manage_directory(self):

        # Making folder which will store files processed
        self.create_root_dir_processed('PROCESSADA')
        self.create_image_year_pathrow_dir()


if __name__ == "__main__":

    mdir = ManagementDirectory(dir_all_targz=sys.argv[1],
                               raster_file_path_targz=sys.argv[2],
                               output_root_dir_image_processed=sys.argv[3])







