import sys


class LandsatFileInfo:

    def __init__(self, raster_file_path_targz):
        # Input row file (landsat file compressed like dowloaded from USGS)
        self.raster_file_path_targz = raster_file_path_targz

    def get_file_name(self):
        """
        Get file name
        :return:
        """
        file_name = str(self.raster_file_path_targz).split('/')[-1][:-7]

        return file_name

    def get_path_row_from_file(self):
        """
        Function to know how path and row from landsat scene
        :return:
        """
        path, row = self.get_file_name()[10:13], self.get_file_name()[13:16]

        return path, row

    def get_aquisition_data_landsat(self):
        """
        Getting aquisition data from landsat file
        :return:
        """
        return self.get_file_name()[17:25]


if __name__ == "__main__":

    lc_info = LandsatFileInfo(raster_file_path_targz=sys.argv[1])
    print(lc_info.get_file_name(),
          lc_info.get_path_row_from_file(),
          lc_info.get_aquisition_data_landsat())