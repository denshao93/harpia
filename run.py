import os #NOQA
import sys
import tempfile #NOQA
import glob
import SatelliteFileInfo as s
import SentinelFileInfo as sen
import LandsatFileInfo as land
import OrganizeDirectory as Od


if __name__ == "__main__":
    # argv[1] = directory where targz files are stored.
    # argv[2] = directory where folder tree will be created to sabe processed
    # files.

    # Create list of zip and tar.gz files from folder where they are store.
    files = [f for f_ in [glob.glob(e)
             for e in (sys.argv[1]+'/*/*.zip', sys.argv[1]+'/*/*.tar.gz')]
             for f in f_]

    for file_path in files:

        # Create tmp director to put all temp files
        # tmp_dir = tempfile.mkdtemp()

        # Create instance of landsat file where scene features are
        sat = s.SatelliteFileInfo(file_path)
        lc = land.LandsatFileInfo(file_path)
        sent = sen.SentinelFileInfo(file_path)

        # Create director where files will be saved
        if sat.is_file_from_landsat():
            od = Od.OrganizeDirectory(
                    root_dir_path=sys.argv[2],
                    satellite_name=lc.get_initials_name().upper(),
                    satellite_index=''.join(lc.get_index()),
                    year=str(lc.get_aquisition_date().year),
                    month=str(lc.get_aquisition_date().month),
                    file_name=lc.get_scene_file_name())

        elif sat.is_file_from_sentinel():
            od = Od.OrganizeDirectory(
                    root_dir_path=sys.argv[2],
                    satellite_name=lc.get_initials_name().upper(),
                    satellite_index=''.join(sent.get_index()),
                    year=str(sent.get_aquisition_date().year),
                    month=str(sent.get_aquisition_date().month),
                    file_name=sent.get_scene_file_name())

        od.create_dir_satellite_index_year_month_file_name()
