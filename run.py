import os #NOQA
import sys
import tempfile
import SatelliteFileInfo as s
import SentinelFileInfo as sen
import LandsatFileInfo as land
import OrganizeDirectory as Od


if __name__ == "__main__":
    # Run Landsat 8 for forest monitoring
    # argv[1] = directory where targz files are stored.
    # argv[2] = directory where folder tree will be created to sabe processed
    # files.
    for subdir, dirs, files in os.walk(sys.argv[1]):
        for file in files:
            print("Processing " + file)
            # File which will unconpress
            file_path = os.path.join(subdir, file)
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
                        satellite_name=lc.get_satellite_alias_name().upper(),
                        satellite_index=''.join(lc.get_landsat_index()),
                        year=str(lc.get_landsat_aquisition_date().year),
                        month=str(lc.get_landsat_aquisition_date().month),
                        file_name=lc.get_satellite_scene_file_name())
                od.create_dir_satellite_index_year_month_file_name()

            elif sat.is_file_from_sentinel():
                od = Od.OrganizeDirectory(
                        root_dir_path=sys.argv[2],
                        satellite_name=lc.get_satellite_alias_name().upper(),
                        satellite_index=''.join(sent.get_sentinel_index()),
                        year=str(sent.get_sentinel_aquisition_date().year),
                        month=str(sent.get_sentinel_aquisition_date().month),
                        file_name=sent.get_satellite_scene_file_name())
                od.create_dir_satellite_index_year_month_file_name()
