
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
    
    def get_output_file_name(self):
        """Name that will be used to save every output file.

        ..note::
            Folder where file will be saved not use this format. It will
            use full name of file.

        ..note::
        <view_date> is when satellite capture imagem (dd/mm/yyyy)

        Return:
            [str] -- The format of string <satellite>_<pathrow>_<view_date>

        """
        # view_date = '{year}' \
        #             '{month}' \
        #             '{day}'.format(
        #                     year=self.get_aquisition_date().year,
        #                     month=f"{self.get_aquisition_date():%m}",
        #                     day=f"{self.get_aquisition_date():%d}")

        # output_name = '{satellite}_' \
        #               '{index}_' \
        #               '{view_date}'.format(
        #                   satellite=self.get_initials_name(),
        #                   index=''.join(self.get_index()),
        #                   view_date=view_date)

        # return output_name

    def get_parameter_from_satellite(self):
        """Dictionary to cadastrete satellite features."""

        dict = {
                # Landsat
                "L[C,T,E]0[5,7,8].*": 
                    {
                    "initials_name":self.get_scene_file_name()[:4],
                    "aquisition_date": self.get_scene_file_name()[17:25],
                    "julian_day": "",
                    "output_name": self.get_output_file_name(),
                    "index":f"{self.get_scene_file_name()[10:13]}"
                            f"{self.get_scene_file_name()[13:16]}"
                    },
                # Sentinel
                "S2A*": 
                    {
                    "initials_name": self.get_scene_file_name()[:3],
                    "aquisition_date": self.get_scene_file_name()[11:19],
                    "utm_zone": self.get_scene_file_name()[39:41],
                    "julian_day": "",
                    "output_name": self.get_output_file_name(),
                    "index": self.get_scene_file_name()[39:44]
                    },
                # Cbers4
                "CBERS.*": 
                    {
                    "initials_name": self.get_scene_file_name()[:5],
                    "aquisition_date": self.get_scene_file_name(),
                    "utm_zone": self.get_output_file_name(),
                    "julian_day": "",
                    "output_name": self.get_scene_file_name()
                    }
                }
        
        # print(dict["S2A"])
        # print(self.get_scene_file_name())
        return dict[self.get_scene_file_name()]


if __name__ == '__main__':

    s = SatelliteFileInfo(file_path="/home/diogocaribe/BRUTA/Sentinel2A/S2A_MSIL1C_20170804T125311_N0205_R052_T24LVK_20170804T125522.zip")
    print(s.get_parameter_from_satellite())