
"""This class collect information from satellite file."""

import re
import datetime
import os #NOQA
import utils as u


class SatelliteFileInfo:
    """Class to read info from file name that come from satellite."""

    def __init__(self, file_path):
        """File from satellite.
        
        The file used to being processed comes from Landsat satellite,
        CBERS4 and Sentinel2.
        """
        self.file_path = file_path

    def get_scene_file_name(self):
        """Get full file name without extensions.

        This name will be used to create folder name to where we save the
        outfile.
        """
        file_name = u.get_base_name(self.file_path).split('.')[0]

        return file_name

    def is_file_from_landsat(self):
        """Check if file is from landsat satellite."""
        
        return self.get_scene_file_name().startswith("L")

    def is_file_from_sentinel(self):
        """Check if file is from sentinel satellite."""
        return self.get_scene_file_name().startswith("S2")
    
    def is_file_from_cbers4(self):
        """Check if file is from sentinel satellite."""
        return self.get_scene_file_name().startswith("CB")
    
    def get_dictionary_key_of_satellite_dict(self):
        """Get short name of satellite."""
        try:

            expression = "L[C,T,E]0[5,7,8]*"
            if re.match(expression, self.get_scene_file_name()):
                return "landsat"
                    
            expression = "CBERS*"
            if re.match(expression, self.get_scene_file_name()):
                return "cbers4"
            
            expression = "S2*"
            if re.match(expression, self.get_scene_file_name()):
                return "sentinel"
        
        except Exception:
            print("Satellite not found.")

    def get_parameter_from_satellite(self):
        """Dictionary to cadastrete satellite features.
        
        This method return dictionary where basic parameters of file 
        can be capture.
        """
        dict = {
                # Landsat
                "landsat": 
                    {
                    "initials_name":self.get_scene_file_name()[:4],
                    "aquisition_date": self.get_scene_file_name()[17:25],
                    "julian_day": self.get_julian_day,
                    "index":f"{self.get_scene_file_name()[10:13]}"
                            f"{self.get_scene_file_name()[13:16]}"
                    },
                # Sentinel
                "sentinel": 
                    {
                    "initials_name": self.get_scene_file_name()[:3],
                    "aquisition_date": self.get_scene_file_name()[11:19],
                    "utm_zone": self.get_scene_file_name()[39:41],
                    "julian_day": self.get_julian_day,
                    "index": self.get_scene_file_name()[39:44]
                    },
                # Cbers4
                "cbers4": 
                    {
                    "initials_name": self.get_scene_file_name()[:5],
                    "aquisition_date": self.get_scene_file_name()[12:20],
                    "julian_day": self.get_julian_day,
                    "index":f"{self.get_scene_file_name()[21:24]}"
                            f"{self.get_scene_file_name()[25:28]}"
                    }
                }

        return dict[self.get_dictionary_key_of_satellite_dict()]
    
    def get_output_file_name(self):
        """Name that will be used to save every output file.

        ..note::
            Folder where file will be saved not use this format. It will
            use full name of file.

        ..note::
        <view_date> is when satellite capture imagem (dd/mm/yyyy)

        Return:
            [str] -- The format of string <satellite>_<index>_<view_date>

        """
        satellite = self.get_parameter_from_satellite()["initials_name"]
        index = self.get_parameter_from_satellite()["index"]
        aquisition_date = self.get_parameter_from_satellite()["aquisition_date"]
    
        output_name = f"{satellite}_{index}_{aquisition_date}"
                          
        return output_name
    
    def get_julian_day(self):
        """Get julian day from gregorian day."""

        # TODO: Study this function to see the logial of this convertion and if it is right
        
        aquisition_date = self.get_parameter_from_satellite()["aquisition_date"]
        fmt = '%Y%m%d'
        dt = datetime.datetime.strptime(aquisition_date, fmt)
        tt = dt.timetuple()
        
        return int(tt.tm_yday)

if __name__ == '__main__':

    s = SatelliteFileInfo(file_path="/test/files/S2A_MSIL1C_20170804T125311_N0205_R052_T24LVK_20170804T125522.zip")
    print(s.get_parameter_from_satellite())
    s = SatelliteFileInfo(file_path="/test/files/CBERS_4_MUX_20170718_151_116_L4_BAND5.zip")
    print(s.get_parameter_from_satellite())
    s = SatelliteFileInfo(file_path="/test/files/LC08_L1GT_037035_20160314_20160314_01_RT.tar.gz")
    print(s.get_parameter_from_satellite())
    s = SatelliteFileInfo(file_path="/test/files/LE07_L1TP_215068_20171205_20171222_01_T1.tar.gz")
    print(s.get_parameter_from_satellite())