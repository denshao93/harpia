import sys

class SatelliteFileInfo:

    def __init__(self, full_scene_name):

        self.full_scene_name = full_scene_name

    def get_satellite_name(self):
        """
        Getting initials from the satellite file own.

            Landsat 08 = lc8

        Returns:
            [string] -- The initials of satellite name
        """
        try:
            if self.full_scene_name[0:4] == "LC08":
                return "lc08"
        except Exception:
            print("Satellite type not found")


class LandsatFileInfo(SatelliteFileInfo):


    def __init__(self, file_name):

        super().__init__(file_name)

    def check_file_is_from_landsat(self):
        """Check if the file comes from landsat satellite.

        Returns:
            [boolean] -- True or False
        """
        return self.get_satellite_name == "LC08"

    # Limiting the methods above to only landsat imagem files
    if check_file_is_from_landsat:

        def get_path_row_from_file(self):
            """
            Function to know how path and row from landsat scene.

            Returns:
                [list] -- List with two values. They represent index to find
                scene of Landsat. They are called as path row.
            """

            path, row = self.full_scene_name[10:13], self.full_scene_name[13:16]

            return path, row

        def get_aquisition_data_landsat(self):
            """
            Getting aquisition data from landsat file.

            Returns:
                [string] -- Date when landsat capture the image from land surface.
            """

            return self.full_scene_name[17:25]
