import os #NOQA
import sys
import glob
import tempfile #NOQA
import ClipRaster as CR
import UnpackFile as UF
import ComposeBands as CB
import CbersFileInfo as CFI
import LandsatFileInfo as LFI
import SentinelFileInfo as SEI
import OrganizeDirectory as OD
import SatelliteFileInfo as SFI


if __name__ == "__main__":
    # argv[1] = directory where targz files are stored.
    # argv[2] = directory where folder tree will be created to sabe processed
    # files.

    # Important variables:
        # output_file_name = name of file without extension less than original
        # Only <satellite>_<index>_<view_date>
        # It is in sublass of satellite (ex. LandsatFileInfo.py)

        # output_dir = directory where results will be stored.
        # It is created by OrganizedDirectory class


    # Create list of zip and tar.gz files from folder where they are store.
    files = [f for f_ in [glob.glob(e)
            for e in (sys.argv[1]+'/*/S2A*.zip',
                      sys.argv[1]+'/*/CBERS*BAND5.zip', 
                      sys.argv[1]+'/*/L*.tar.gz')]
            for f in f_]

    for file_path in files:
        
        print(file_path)

        # Create tmp director to put all temp files
        tmp_dir = tempfile.mkdtemp()
        
        # Create instance of landsat file where scene features are
        sat = SFI.SatelliteFileInfo(file_path)
        land = LFI.LandsatFileInfo(file_path)
        sent = SEI.SentinelFileInfo(file_path)
        cbers = CFI.CbersFileInfo(file_path)

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

        elif sat.is_file_from_cbers4():
            od = OD.OrganizeDirectory(
                    root_dir_path=sys.argv[2],
                    satellite_name=sat.get_initials_name().upper(),
                    satellite_index=''.join(cbers.get_index()),
                    year=str(cbers.get_aquisition_date().year),
                    month=str(cbers.get_aquisition_date().month),
                    file_name=cbers.get_scene_file_name()[:-6])

        # Create directory to save results
        output_dir = od.create_output_dir()

        # Cbers4
        if sat.is_file_from_cbers4():
            exp = f"{sys.argv[1]}/*/{cbers.get_scene_file_name()[:-6]}*.zip"
            for i in glob.glob(exp):
                up = UF.UnpackFile(file_path=i, tmp_dir=tmp_dir)
                up.uncompress_zip()
            # Stack images
            # Bands: 6 = Blue | 6 = Green | 7 = Red | 8 = Nir |
            bands_expression = '5-8'
            expression = f"CBERS*BAND[{bands_expression}].tif"
            CB.ComposeBands(input_dir=tmp_dir,
                            output_dir=tmp_dir,
                            output_file_name=cbers.get_output_file_name())\
                            .stack_img(expression=expression,
                                       extension = '.TIF')
            # Clip
            img_path = f"{tmp_dir}/r{cbers.get_output_file_name()}.TIF"
            CR.ClipRaster(img_path=img_path, tmp_dir=tmp_dir, 
                          scene_file_name=cbers.get_scene_file_name()[:-6],
                          output_dir = output_dir, 
                          output_file_name = cbers.get_output_file_name()).run_clip()
            # Segmentation
            # Cloud/Shadow
            continue
        # Create objet to unpack files
        up = UF.UnpackFile(file_path=file_path, tmp_dir=tmp_dir)

        # Work with Sentinel2
        if sat.is_file_from_sentinel():
            # Unzip setinel file
            up.uncompress_zip()

            # Compose bands with 10m spatial resolution
            CB.ComposeBands(input_dir=tmp_dir,
                            output_dir=od.create_output_dir(),
                            output_file_name=sent.get_output_file_name()) \
            .stack_sentinel(scene_file_name=sent.get_scene_file_name(),
                            utm_zone=sent.get_utm_zone())
            # Clip
            img_path = f"{tmp_dir}/r{sent.get_output_file_name()}.TIF"
            CR.ClipRaster(img_path=img_path, tmp_dir=tmp_dir, 
                          scene_file_name=sent.get_scene_file_name(),
                          output_dir = output_dir, 
                          output_file_name = sent.get_output_file_name()).run_clip()
            # Segmentation
            # Cloud/Shadow
            continue
        
        # Work with Landsat 8
        elif sat.get_initials_name() == 'LC08':
            # Set bands to unpack from landsat 8
            bands=[1,2,3,4,5,6,7,9,10,11]
            # Stack images
            # Bands: 3 = Green | 4 = Red | 5 = Nir | 6 = Swir1 |
            bands_expression = '3-6'

        # Work with Landsat 5 and 7
        elif sat.is_file_from_landsat():
            # Set bands to unpack from landsat 5 and 7
            bands=[2,3,4,5]
            # Stack images
            # Bands: 2 = Green | 3 = Red | 4 = Nir | 5 = Swir |
            bands_expression = '2-5'
            # Clip

        # Unpack files from landsat
        up.uncompres_file(bands)

        # Stack bands from landsat
        expression = "L[C,T,E]0[5,7,8]*_B[{bands_expression}].TIF" \
                    .format(bands_expression=bands_expression)
        CB.ComposeBands(input_dir=tmp_dir,
                        output_dir=tmp_dir,
                        output_file_name=land.get_scene_file_name()) \
                        .stack_img(expression=expression,
                                extension = '.TIF')
        # Clip
        # Segmentation
        # Cloud/Shadow
            # Thinking about compose image in fuction for fmask
        img_path = f"{tmp_dir}/{land.get_scene_file_name()}.TIF"
        CR.ClipRaster(img_path=img_path, tmp_dir=tmp_dir, 
                        scene_file_name=land.get_scene_file_name(),
                        output_dir = output_dir, 
                        output_file_name = land.get_output_file_name()).run_clip()