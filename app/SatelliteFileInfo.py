"""This class collect information from satellite file."""
import os
import re
import datetime
import utils as u
import pandas as pd
from pathlib import Path
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

    @staticmethod
    def _read_satallite_data_table():
        """ Read table where to register satallite from image file."""
        csv_path = Path('app/data/table/satallite_data.csv')
        df = pd.read_csv(csv_path, sep=',')

        return df

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

    def _which_cbers4_sensor(self):
        """Answer if file come from MUX sensor of Cbers 4 satellite."""
        if self.is_cbers4_file() and 'MUX' in self.get_scene_file_name():
            
            return 'mux'

        elif self.is_cbers4_file() and 'AWFI' in self.get_scene_file_name():
    
            return 'awfi'
    
    def _get_path_row_from_file_landsat(self):
        """."""
        satellite_table = self._read_satallite_data_table()
        scene_file_name = self.get_scene_file_name()
        satellite_name = self.get_satellite_name_from_file()

        satallite_row_data_table = satellite_table['name'] == satellite_name

        # Path
        slice_path = satellite_table.loc[satallite_row_data_table,
                                                "path"].values[0]     
        path = eval('scene_file_name[' + slice_path + ']')

        # Row
        slice_row = satellite_table.loc[satallite_row_data_table,
                                                "row"].values[0]     
        row = eval('scene_file_name[' + slice_row + ']')

        path_row = f'{path}{row}'

        return path_row
   
    def _get_path_row_from_file_cbers(self):
        """."""
        satellite_table = self._read_satallite_data_table()
        scene_file_name = self.get_scene_file_name()
        satellite_name = self.get_satellite_name_from_file()
        satallite_row_data_table = satellite_table['name'] == satellite_name

        # Path
        slice_path = satellite_table.loc[satallite_row_data_table,
                                                "path"].values[0] 
        slice_row = satellite_table.loc[satallite_row_data_table,
                                                "row"].values[0] 
        slice_path = slice_path.split(',')
        slice_row = slice_row.split(',')
        
        if self._which_cbers4_sensor() == 'mux':
            slice_path = slice_path[0]
            slice_row = slice_row[0]

        elif self._which_cbers4_sensor() == 'awfi':
            slice_path = slice_path[1]
            slice_row = slice_row[1]
        
        path = eval('scene_file_name[' + slice_path + ']')
        row = eval('scene_file_name[' + slice_row + ']')
        
        path_row = f'{path}{row}'

        return path_row

    def get_parameter_satellite(self):
        """."""
        satellite_table = self._read_satallite_data_table()
        scene_file_name = self.get_scene_file_name()
        satellite_name = self.get_satellite_name_from_file()

        satallite_row_data_table = satellite_table['name'] == satellite_name

        # Initial name
        slice_initial_name = satellite_table.loc[satallite_row_data_table,
                                         "satellite_initial_name"].values[0]     
        initials_name = eval('scene_file_name[' + slice_initial_name + ']')

        # Sensor
        if self.is_cbers4_file():
            sensor = self._which_cbers4_sensor()
            
        else:
            slice_sensor = satellite_table.loc[satallite_row_data_table,
                                                "sensor"].values[0]     
            sensor = eval('scene_file_name[' + slice_sensor + ']')
        
        # Acquisition Date
        slice_acquisition_date = satellite_table.loc[satallite_row_data_table,
                                         "acquisition_date"].values[0]     
        acquisition_date = eval('scene_file_name[' + slice_acquisition_date + ']')

        # Index
        if self.is_landsat_file():
            index = self._get_path_row_from_file_landsat()
        
        elif self.is_sentinel_file():
            slice_index = satellite_table.loc[satallite_row_data_table,
                                         "tile"].values[0]     
            tile = eval('scene_file_name[' + slice_index + ']')
            
            index = tile
        
        elif self.is_cbers4_file():
            index = self._get_path_row_from_file_cbers()
    
        dict = {"initials_name": initials_name,
                "sensor": sensor,
                "scene_file_name": scene_file_name,
                "aquisition_date": acquisition_date,
                "index": index
                }

        return dict

    def get_satellite_name_from_file(self):
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

    def _get_month_resourcesat2(self):
        """Get month as cardinal number from ResourceSat2 satellite"""
        if self.is_resourcesat2_file(): 
            month = self.get_scene_file_name()[7:10]
            return MD.month_R2LS3[month]
            
if __name__ == '__main__':

    s = SatelliteFileInfo(file_path="/test/files/S2A_MSIL1C_20170804T125311_N0205_R052_T24LVK_20170804T125522.zip")
    print(s.get_parameter_satellite())
    s = SatelliteFileInfo(file_path="/test/files/CBERS_4_MUX_20170718_151_116_L4_BAND5.zip")
    print(s.get_parameter_satellite())
    s = SatelliteFileInfo(file_path="/test/files/CBERS_4_AWFI_20180729_173_135_L4_BAND13.zip")
    print(s.get_parameter_satellite())
    s = SatelliteFileInfo(file_path="/test/files/LC08_L1GT_037035_20160314_20160314_01_RT.tar.gz")
    print(s.get_parameter_satellite())
    s = SatelliteFileInfo(file_path="/test/files/LE07_L1TP_215068_20171205_20171222_01_T1.tar.gz")
    print(s.get_parameter_satellite())
    s = SatelliteFileInfo(file_path="/test/files/LT05_L1TP_220069_20110903_20161008_01_T1.tar.gz")
    print(s.get_parameter_satellite())
    # s = SatelliteFileInfo(file_path="/test/files/R2LS326JUL2018336087STUC00GODP_BAND2_RPC.tif.zip")
    # print(s.get_initial_name())