"""This class collect information from satellite file."""
import utils as u
from SatelliteFileInfo import SatelliteFileInfo


class LandsatFileInfo(SatelliteFileInfo):
    """Get landsat information from targz file."""

    def __init__(self, file_path):
        """."""
        super().__init__(file_path)

    # Limiting the methods above to only landsat imagem files

    def get_collection(self):
        """Get what collection landsat file belongs.

        Return:
            1 = Collection 1
            2 = Collection 2
            3 = Real Time
        """
        if self.get_scene_file_name().endwith('T1'):
            # Collection 1
            return 1
        elif self.get_scene_file_name().endwith('T2'):
            # Collection 2
            return 2
        elif self.get_scene_file_name().endwith('RT'):
            # Collection Real time
            return 3

    def get_index(self):
        """Know how path and row from landsat scene.

        Path row is index where find scene of landsat files.

        Return:
            [list] -- List with two values. They represent index to find
            scene of Landsat. They are called as path row.
        """
        path, row = (self.get_scene_file_name()[10:13],
                     self.get_scene_file_name()[13:16])

        return [path, row]

    def get_aquisition_date(self):
        """Get aquisition data from landsat file.

        Return:
            [dateandtime.date] -- Date when landsat capture the image from
                                  land surface.
        """
        date = u.int2date(int(self.get_scene_file_name()[17:25]))

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
                            month=self.get_aquisition_date().month,
                            day=self.get_aquisition_date().day)

        output_name = '{satellite}_' \
                      '{index}_' \
                      '{view_date}'.format(
                          satellite=self.get_initials_name(),
                          index=''.join(self.get_index()),
                          view_date=view_date)

        return output_name
