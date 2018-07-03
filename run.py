import os #NOQA
import sys
import glob
import tempfile #NOQA
import ComposeBands as CB
import UncompressFile as UF
import LandsatFileInfo as LFI
import SatelliteFileInfo as SFI
import SentinelFileInfo as SFI
import OrganizeDirectory as OD


if __name__ == "__main__":
    # argv[1] = directory where targz files are stored.
    # argv[2] = directory where folder tree will be created to sabe processed
    # files.

    # Important variables:
        # output_file_name = name of file without extension
        # It is in sublass of satellite (ex. LandsatFileInfo.py)

        # output_dir = directory where results will be stored.
        # It is created by OrganizedDirectory class


    # Create list of zip and tar.gz files from folder where they are store.
    files = [f for f_ in [glob.glob(e)
             for e in (sys.argv[1]+'/*/*.zip', sys.argv[1]+'/*/*.tar.gz')]
             for f in f_]

    for file_path in files:

        # Create tmp director to put all temp files
        tmp_dir = tempfile.mkdtemp()

        # Create instance of landsat file where scene features are
        sat = SFI.SatelliteFileInfo(file_path)
        land = LFI.LandsatFileInfo(file_path)
        sent = SFI.SentinelFileInfo(file_path)

        # Create director where files will be saved
        if sat.is_file_from_landsat():
            od = OD.OrganizeDirectory(
                    root_dir_path=sys.argv[2],
                    satellite_name=land.get_initials_name().upper(),
                    satellite_index=''.join(land.get_index()),
                    year=str(land.get_aquisition_date().year),
                    month=str(land.get_aquisition_date().month),
                    file_name=land.get_scene_file_name())

        elif sat.is_file_from_sentinel():
            od = OD.OrganizeDirectory(
                    root_dir_path=sys.argv[2],
                    satellite_name=land.get_initials_name().upper(),
                    satellite_index=''.join(sent.get_index()),
                    year=str(sent.get_aquisition_date().year),
                    month=str(sent.get_aquisition_date().month),
                    file_name=sent.get_scene_file_name())

        od.create_output_dir()

        # Uncompress file
        UF.UncompressFile(file_path=file_path, tmp_dir=tmp_dir).uncompres_file()

        # Stacking imagem to clip
        
        # expression="LC08*_B[3-6].TIF")

