import os #NOQA
import MonthDictionary as m


class OrganizeDirectory:
    """Create tree of directory to save processed file organized."""

    processed_directory_name = 'PROCESSADA'

    def __init__(self,
                 root_dir_path,
                 satellite_name,
                 satellite_index,
                 year,
                 month,
                 file_name):
        """.

        Args:
            root_dir_path (str): Root directory given by user. It is where tree
                    folder will be created to store files processed.
            satellite_name (str): Value that represent scene from satellite.
            satellite_index (str):
            year (int): From aquisition date of satellite scene.
            month (int): From aquisition date of satellite scene.
            file_name (str): Full name of scene

        """
        self.root_dir_path = root_dir_path
        self.satellite_name = satellite_name
        self.satellite_index = satellite_index
        self.year = year
        self.month = month
        self.file_name = file_name

    def create_root_dir_path(self, processed_directory_name):
        """Create directory where files will be organized."""
        dir_path = os.path.join(self.root_dir_path, processed_directory_name)

        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        return dir_path

    def get_mounth_folder_name(self):
        """Do the name of month with cardinal and literal word of monthself."""
        string_mounth = m.month[int(self.month)]

        month_folder_name = '{}_{}'.format(self.month, string_mounth)

        return month_folder_name

    def create_output_dir(self):
        """Create directory where file processed will be saved.

        ..note::
            <root_dir_path> = Root place given by parameters
            <processed_directory_name> = Set in variable
                                         processed_directory_name
            <satellite_name> = Sigle words wchich represent satellite name
            <index_of_satelite> = Value that represent scene from satellite.
            <year> = From aquisition date.
            <month> = From aquisition date.
            <file_name> = Full name of scene
        """
        dir_path = os.path.join(self.root_dir_path,
                                self.processed_directory_name,
                                self.satellite_name,
                                self.satellite_index,
                                self.year,
                                self.get_mounth_folder_name(),
                                self.file_name)

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        return dir_path
