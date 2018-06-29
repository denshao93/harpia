
"""This class collect information from satellite file."""

import os


class SatelliteFileInfo:
    """Class to read info from targz file name."""

    def __init__(self, file_path):
        """."""
        # The file can be targz or another one.
        # The rotine is created running targz file from landsat satellite but
        # we hope that this class be general enough to read another kind of
        # files.
        self.file_path = file_path

    def get_base_name(self):
        """Get basename from targz file path.

        Base name is file name with extension.
        """
        base_name = os.path.basename(self.file_path)

        return base_name

    def get_file_name(self):
        """Get full file name without extensions.

        This name will be used to create folder name to where we save the
        outfile.
        """
        file_name = self.get_base_name().split()[0]

        return file_name

    def get_satellite_name(self):
        """Get initials letters from the satellite file to know who it is.

        Return:
            [str] -- The initials letters from satellite name.
        """
        try:
            if self.get_base_name[0:4] == "LC08":
                return "lc08"
            elif self.get_base_name[0:4] == "LC07":
                return "lc07"
            elif self.get_base_name[0:4] == "LC05":
                return "lc05"
        except Exception:
            print("Satellite type not found")


class LandsatFileInfo(SatelliteFileInfo):
    """Get landsat information from targz file."""

    def __init__(self, file_name):
        """."""
        super().__init__(file_name)

    def check_file_is_landsat(self):
        """Check if the file comes from landsat satellite.

        Return:
            [bool] -- True or False
        """
        return self.get_base_name[0:4].lower() in ("lc05", "lc07", "lc08")

    # Limiting the methods above to only landsat imagem files
    if check_file_is_landsat:

        def get_path_row(self):
            """Know how path and row from landsat scene.

            Path row is index where find scene of landsat files.

            Return:
                [list] -- List with two values. They represent index to find
                scene of Landsat. They are called as path row.
            """
            path, row = self.get_file_name[10:13], self.get_file_name[13:16]

            return path, row

        def get_aquisition_data_landsat(self):
            """Get aquisition data from landsat file.

            Return:
                [str] -- Date when landsat capture the image from land surface.
            """
            return self.get_file_name[17:25]

        def get_output_name_file(self):
            """Name that will be used to save every output file.

            ..note::
                Folder where file will be saved not use this format. It will
                use full name of file.

            ..note::
            <view_date> is when satellite capture imagem (dd/mm/yyyy)

            Return:
                [str] -- The format of string <satellite>_<pathrow>_<view_date>

            """
            output_name = '{satellite}_' \
                          '{pathrow}_' \
                          '{view_date}'.format(self.get_satellite_name(),
                                               self.get_path_row(),
                                               self.view_date())

            return output_name
