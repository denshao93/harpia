"""This class collect information from satellite file."""
import utils as u
from SatelliteFileInfo import SatelliteFileInfo


class CbersFileInfo(SatelliteFileInfo):
    """Get cerbers4 information from file."""

    def __init__(self, file_path):
        """."""
        super().__init__(file_path)

    def get_index(self):
        """Know how path and row from cebers4 scene.

        Path row is index where find scene of cebers files.

        Return:
            [list] -- List with two values. They represent index to find
            scene of Landsat. They are called as path row.
        """
        index = f"{self.get_scene_file_name()[21:24]}" \
                f"{self.get_scene_file_name()[25:28]}"

        return index

    def get_aquisition_date(self):
        """Get aquisition data from Cebers4 file.

        Return:
            [dateandtime.date] -- Date when Cebers 4 capture the image from
                                  land surface.
        """
        date = u.int2date(int(self.get_scene_file_name()[12:20]))

        return date


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
        view_date = '{year}' \
                    '{month}' \
                    '{day}'.format(
                            year=self.get_aquisition_date().year,
                            month=f"{self.get_aquisition_date():%m}",
                            day=f"{self.get_aquisition_date():%d}")

        output_name = '{satellite}_' \
                      '{index}_' \
                      '{view_date}'.format(
                          satellite=self.get_initials_name(),
                          index=''.join(self.get_index()),
                          view_date=view_date)

        return output_name
