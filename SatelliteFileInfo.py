
"""This class collect information from satellite file."""

import os #NOQA
import utils as u


class SatelliteFileInfo:
    """Class to read info from file name that come from satellite."""

    def __init__(self, file_path):
        """."""
        # The file can be targz or another one.
        # The rotine is created running targz file from landsat satellite but
        # we hope that this class be general enough to read another kind of
        # files.
        self.file_path = file_path

    def get_scene_file_name(self):
        """Get full file name without extensions.

        This name will be used to create folder name to where we save the
        outfile.
        """
        file_name = u.get_base_name(self.file_path).split('.')[0]

        return file_name

    def get_initials_name(self):
        """Get initials letters from the satellite file to know who it is.

        Return:
            [str] -- The initials letters from satellite name.
        """
        try:

            if self.is_file_from_landsat():
                return self.get_scene_file_name()[:4]
            elif self.is_file_from_sentinel():
                return self.get_scene_file_name()[:3]
            elif self.is_file_from_cbers4():
                return self.get_scene_file_name()[:5]
                
        except Exception:
            print("Satellite type not found")

    def is_file_from_landsat(self):
        """Check if file is from landsat satellite."""
        return self.get_scene_file_name().startswith("L")

    def is_file_from_sentinel(self):
        """Check if file is from sentinel satellite."""
        return self.get_scene_file_name().startswith("S2")
    
    def is_file_from_cbers4(self):
        """Check if file is from sentinel satellite."""
        return self.get_scene_file_name().startswith("CB")
