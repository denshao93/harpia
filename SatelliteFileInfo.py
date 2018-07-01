
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

    def get_satellite_base_name_file(self):
        """Get basename from targz file path.

        Base name is file name with extension.
        """
        base_name = os.path.basename(self.file_path)

        return base_name

    def get_satellite_file_name(self):
        """Get full file name without extensions.

        This name will be used to create folder name to where we save the
        outfile.
        """
        file_name = self.get_satellite_base_name_file().split('.')[0]

        return file_name

    def get_satellite_name(self):
        """Get initials letters from the satellite file to know who it is.

        Return:
            [str] -- The initials letters from satellite name.
        """
        try:
            if self.get_satellite_base_name_file()[0:4] == "LC08":
                return "lc08"
            elif self.get_satellite_base_name_file()[0:4] == "LC07":
                return "lc07"
            elif self.get_satellite_base_name_file()[0:4] == "LC05":
                return "lc05"
        except Exception:
            print("Satellite type not found")
