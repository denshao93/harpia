import sys


class LandsatFileInfo:

    def __init__(self, metadata_path):

        self.metadata_path = metadata_path

    def read_lc8_metadata(self):
        """
        Reading metadata file (MTL.txt) from landsat 8 image
        :return:
        """
        f = open(self.metadata_path, 'r')  # open file for reading
        output = {}  # Dict
        for line in f.readlines():  # Iterates through every line in the string
            if "=" in line:  # make sure line has data as wanted
                l = line.split("=")  # Seperate by "=" and put into a list
                output[l[0].strip()] = l[1].strip()  # First word is key, second word is value

        return output  # Returns a dictionary with the key, value pairs.

        data = build_data(f)

        return data

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