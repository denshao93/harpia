"""This class collect information from satellite file."""
import os #NOQA
import re
import datetime
import utils as u
import MonthDictionary as MD


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

    def is_landsat_file(self):
        """Check if file is from landsat satellite."""
        
        return self.get_scene_file_name().startswith("L")

    def is_sentinel_file(self):
        """Check if file is from sentinel satellite."""
        return self.get_scene_file_name().startswith("S2")
    
    def is_cbers4_file(self):
        """Check if file is from sentinel satellite."""
        return self.get_scene_file_name().startswith("CB")
    
    def is_resourcesat2_file(self):
        """Check if file is from sentinel satellite."""
        return self.get_scene_file_name().startswith("R2")
    
    def get_dictionary_key_satellite_dict(self):
        """Get short name of satellite."""
        try:

            expression = "L[C,T,E]0[5,7,8]*"
            if re.match(expression, self.get_scene_file_name()):
                return "landsat"
                    
            expression = "CBERS*"
            if re.match(expression, self.get_scene_file_name()):
                return "cbers4"
            
            expression = "S2A*"
            if re.match(expression, self.get_scene_file_name()):
                return "sentinel"
            
            expression = "R2*"
            if re.match(expression, self.get_scene_file_name()):
                return "resourcesat2"
        
        except Exception:
            print("Satellite not found.")
    
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
        satellite = self.get_parameter_satellite()["initials_name"]
        index = self.get_parameter_satellite()["index"]
        aquisition_date = self.get_parameter_satellite()["aquisition_date"]
    
        output_name = f"{satellite}_{index}_{aquisition_date}"
                          
        return output_name
    
    def get_julian_day_aquisition_date(self, dict):
        """Get julian day from gregorian day."""
        # TODO: Study this function to see the logial of this convertion and if it is right
        aquisition_date = dict["aquisition_date"]
        fmt = '%Y%m%d'
        dt = datetime.datetime.strptime(aquisition_date, fmt)
        tt = dt.timetuple()
        
        return tt.tm_yday
    
    def get_days_from_today(self, dict):
        """Calc howm many days from processing days.
        
        It is calc to decide if image will passed in monitoring forest process
        """ 
        date_today = datetime.date.today().strftime('%Y%m%d')
        fmt = '%Y%m%d'
        dt = datetime.datetime.strptime(date_today, fmt)
        tt = dt.timetuple()
        
        # TODO: Result is wrong. See it again.
        day_from_today = tt.tm_yday - dict["julian_day"]

        return day_from_today

    def __get_month_resourcesat2(self):
        """Get month as cardinal number from ResourceSat2 satellite"""
        if self.is_resourcesat2_file(): 
            month = self.get_scene_file_name()[7:10]
            return MD.month_R2LS3[month]

    def get_parameter_satellite(self):
        """Dictionary to cadastrete satellite features.
        
        This method return dictionary where basic parameters of file 
        can be capture.
        """
        scene_file_name = self.get_scene_file_name()
        try:
            dict = {
                    # Landsat
                    "landsat": 
                        {
                        "initials_name": scene_file_name[:4],
                        "sensor": scene_file_name[1:2],
                        "scene_file_name": scene_file_name,
                        "aquisition_date": scene_file_name[17:25],
                        "aquisition_year": scene_file_name[17:21],
                        "aquisition_month": scene_file_name[21:23],
                        "aquisition_day": scene_file_name[23:25],
                        "julian_day": "",
                        "days_from_today": "",
                        "index":f"{scene_file_name[10:13]}"
                                f"{scene_file_name[13:16]}"
                        },
                    # Sentinel
                    "sentinel": 
                        {
                        "initials_name": scene_file_name[:3],
                        "sensor": scene_file_name[4:7],
                        "scene_file_name": scene_file_name,
                        "aquisition_date": scene_file_name[11:19],
                        "aquisition_year": scene_file_name[11:15],
                        "aquisition_month": scene_file_name[15:17],
                        "aquisition_day": scene_file_name[17:19],
                        "utm_zone": scene_file_name[39:41],
                        "julian_day": "",
                        "days_from_today": "",
                        "index": scene_file_name[39:44]
                        },
                    # Cbers4
                    "cbers4": 
                        {
                        "initials_name": scene_file_name[:5],
                        "sensor": scene_file_name[8:11],
                        "scene_file_name": scene_file_name[:-6],
                        "aquisition_date": scene_file_name[12:20],
                        "aquisition_year": scene_file_name[12:16],
                        "aquisition_month": scene_file_name[16:18],
                        "aquisition_day": scene_file_name[18:20],
                        "julian_day": "",
                        "days_from_today": "",
                        "index":f"{scene_file_name[21:24]}"
                                f"{scene_file_name[25:28]}"
                        },
                        # Resoucesat2
                    "resourcesat2": 
                        {
                        "initials_name": scene_file_name[:5],
                        "sensor": scene_file_name[2:5],
                        "scene_file_name": scene_file_name[:-10],
                        "aquisition_date":  f"{scene_file_name[10:14]}"
                                            f"{self.__get_month_resourcesat2()}"
                                            f"{scene_file_name[5:7]}",
                        "aquisition_year": scene_file_name[10:14],
                        "aquisition_month": self.__get_month_resourcesat2(),
                        "aquisition_day": scene_file_name[5:7],
                        "julian_day": "",
                        "days_from_today": "",
                        "index":scene_file_name[14:20]                            
                        }
                    }
            
            dict = dict[self.get_dictionary_key_satellite_dict()]
            
            # Add julian day and how many days image will be processed.
            dict["julian_day"] = self.get_julian_day_aquisition_date(dict)
            
            # dict["days_from_today"] = self.get_days_from_today(dict)

            return dict

        except Exception:
            dict = {}
            scene_file_name = self.get_scene_file_name()
            if self.is_cbers4_file and self.get_scene_file_name()[9:12] == 'WFI':
                dict = {
                # Cbers4
                    "initials_name": scene_file_name[:5],
                    "sensor": scene_file_name[9:12],
                    "scene_file_name": scene_file_name[:-7],
                    "aquisition_date": scene_file_name[13:21],
                    "aquisition_year": scene_file_name[13:17],
                    "aquisition_month": scene_file_name[17:19],
                    "aquisition_day": scene_file_name[19:21],
                    "julian_day": "",
                    "days_from_today": "",
                    "index":f"{scene_file_name[22:25]}"
                            f"{scene_file_name[26:29]}"
                    }
        
            # Add julian day and how many days image will be processed.
            dict["julian_day"] = self.get_julian_day_aquisition_date(dict)
            
            # dict["days_from_today"] = self.get_days_from_today(dict)

            return dict
            


if __name__ == '__main__':

    # s = SatelliteFileInfo(file_path="/test/files/S2A_MSIL1C_20170804T125311_N0205_R052_T24LVK_20170804T125522.zip")
    # print(s.get_parameter_satellite())
    # s = SatelliteFileInfo(file_path="/test/files/CBERS_4_MUX_20170718_151_116_L4_BAND5.zip")
    # print(s.get_parameter_satellite())
    s = SatelliteFileInfo(file_path="/test/files/CBERS_4_AWFI_20180729_173_135_L4_BAND13.zip")
    print(s.get_parameter_satellite())
    # s = SatelliteFileInfo(file_path="/test/files/LC08_L1GT_037035_20160314_20160314_01_RT.tar.gz")
    # print(s.get_parameter_satellite())
    # s = SatelliteFileInfo(file_path="/test/files/LE07_L1TP_215068_20171205_20171222_01_T1.tar.gz")
    # print(s.get_parameter_satellite())
    # s = SatelliteFileInfo(file_path="/test/files/LT05_L1TP_220069_20110903_20161008_01_T1.tar.gz")
    # print(s.get_parameter_satellite())
    # s = SatelliteFileInfo(file_path="/test/files/R2LS326JUL2018336087STUC00GODP_BAND2_RPC.tif.zip")
    # print(s.get_parameter_satellite())