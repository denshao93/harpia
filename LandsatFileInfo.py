import sys


class LandsatFileInfo:

    def __init__(self, file_name):
        
        self.file_name = file_name
    
    def get_path_row_from_file(self):
        """
        Function to know how path and row from landsat scene
        :return:
        """
        path, row = self.file_name[10:13], self.file_name[13:16]

        return path, row

    def get_aquisition_data_landsat(self):
        """
        Getting aquisition data from landsat file
        :return:
        """
        return self.file_name()[17:25]


# if __name__ == "__main__":

#     lc_info = LandsatFileInfo()
#     print(lc_info.get_file_name(),
#           lc_info.get_path_row_from_file(),
#           lc_info.get_aquisition_data_landsat())