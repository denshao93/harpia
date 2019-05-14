import csv
import datetime
import glob
import os  # NOQA
import shutil
import sys
import tempfile  # NOQA
from pathlib import Path
from os.path import join

import yaml
import ClipRaster as CR
import CloudShadowLC8 as CL
import ComposeBands as CB
import Connection2Database as CDB
import ConnectionDB as C
import LoadSegmentationDatabase as LSD
import OrganizeDirectory as OD
import PyramidRaster as PR
import Raster as R
import RasterReproject as RR
import SatelliteFileInfo as SFI
import Segmetation as SEG
import UnpackFile as UF

# Write log of scene processed in csv
# Open yaml 
# Open yaml 
with open(Path("app/config/const.yaml"), 'r') as f:
        const = yaml.safe_load(f)

def save_datetime_file_processig(scene_title):
    conn_string = const['db']
    con = C.Connection(conn_string)
    query = f"UPDATE metadado_img.metadado_sentinel SET date_file_processing = current_timestamp WHERE title = '{scene_title}';"
    con.run_update(query)

if __name__ == "__main__":
    # argv[1] = directory where targz files are stored.
    # argv[2] = directory where folder tree will be created to save processed
    # files.

    # Important variables:
        # output_file_name = name of file without extension less than original
        # Only <satellite>_<index>_<view_date>
        # It is in sublass of satellite (ex. LandsatFileInfo.py)

        # output_dir = directory where results will be stored.
        # It is created by OrganizedDirectory class

    # Create list of zip and tar.gz files from folder where they are store.
    files = [f for f_ in [glob.glob(e)
                          for e in (sys.argv[1]+'/*/S2*.zip',
                                    sys.argv[1]+'/*/CBERS*BAND5.zip',
                                    sys.argv[1]+'/*/CBERS*BAND2.zip',
                                    sys.argv[1]+'/*/CBERS*BAND13.zip',
                                    sys.argv[1]+'/*/R2*BAND5*.zip',
                                    sys.argv[1]+'/*/L*.tar.gz')]
             for f in f_]
    
    
    for file_path in files:
        
        print(file_path)
        now = datetime.datetime.now()

        # Create tmp director to put all temp files
        tmp_dir = tempfile.mkdtemp()

        # Create instance of landsat file where scene features are
        sat = SFI.SatelliteFileInfo(file_path)

        parameter_satellite = sat.get_parameter_satellite()
        output_file_name = sat.get_output_file_name()
        scene_file_name = parameter_satellite["scene_file_name"]

        # Csv parameters for log
        home_path = str(Path.home())
        csv_path = str(Path('workspace/harpia/app/log/log.csv'))
        csv_path = f'{home_path}/{csv_path}'
        
        # Create director where files will be saved
        od = OD.OrganizeDirectory(root_dir_path=sys.argv[2],
                                  satellite_name=parameter_satellite["initials_name"],
                                  satellite_index=parameter_satellite["index"],
                                  year=parameter_satellite["aquisition_year"],
                                  month=parameter_satellite["aquisition_month"],
                                  file_name=parameter_satellite["scene_file_name"])

        # Create directory to save results
        output_dir = od.create_output_dir()

        # Instatiation segmentation class
        s = SEG.Segmentation(output_dir=output_dir, tmp_dir=tmp_dir,
                             output_file_name=sat.get_output_file_name())

        l = LSD.LoadSegmentationDatabase(tmp_dir=tmp_dir,
                                         satellite_parameters=parameter_satellite,
                                         output_file_name=sat.get_output_file_name())

        #####################################################################################
        ################################### Cbers4/ResorceSat2###############################
        #####################################################################################
        if sat.is_cbers4_file() or sat.is_resourcesat2_file():
            exp = f"{sys.argv[1]}/*/{sat.get_parameter_satellite()['scene_file_name'][:-1]}*.zip"
            for i in glob.glob(exp):
                up = UF.UnpackFile(file_path=i, tmp_dir=tmp_dir)
                up.uncompress_zip()
            # Stack images
            # Bands: 5 = Blue | 6 = Green | 7 = Red | 8 = Nir |
            if sat.is_cbers4_file():
                bands_expression = '5-8'
                band_order = [4, 3, 2, 1]
                expression = f"CBERS*BAND[{bands_expression}].tif"

                if parameter_satellite['sensor'] == 'WFI':
                    bands_expression = f"1[3-6]"
                    expression = f"CBERS*BAND{bands_expression}.tif"
                
                elif parameter_satellite['sensor'] == 'pan10m':
                    bands_expression = f"[2-4]"
                    expression = f"CBERS*BAND{bands_expression}.tif"
                    band_order = [3, 2, 1]

            elif sat.is_resourcesat2_file():
                bands_expression = '2-5'
                expression = f"R2*BAND[{bands_expression}]*.tif"
                band_order = [3, 2, 1, 4]

            CB.ComposeBands(input_dir=tmp_dir,
                            output_dir=tmp_dir,
                            output_file_name=sat.get_output_file_name())\
                .stack_img(expression=expression,
                           extension='.TIF')

            # Reproject to Sirgas 2000
            input_img_path = os.path.join(
                tmp_dir, f"{sat.get_output_file_name()}.TIF")
            output_img_path = os.path.join(
                tmp_dir, f"r{sat.get_output_file_name()}.TIF")

            rprj = RR.RasterReproject(input_img_path, output_img_path)
            rprj.reproject_raster_to_epsg4674()

            # Clip
            img_path = f"{tmp_dir}/r{sat.get_output_file_name()}.TIF"

            c = CR.ClipRaster(img_path=img_path, tmp_dir=tmp_dir,
                              scene_file_name=sat.get_parameter_satellite()[
                                  "scene_file_name"],
                              output_dir=output_dir,
                              output_file_name=sat.get_output_file_name())

            r = R.Raster(img_path=img_path)

            if r.intersects_trace_outline_aoi():
                c.clip_raster_by_mask(band_order)
            else:
                import RasterTranslate as RT
                rt = RT.RasterTranslate(img_path=img_path,
                                        output_dir=output_dir,
                                        output_file_name=sat.get_output_file_name())
                rt.translate_8bit(band_order)

            # Make pyramid
            img_path = os.path.join(
                output_dir, f"{sat.get_output_file_name()}.TIF")
            PR.PyramidRaster(img_path=img_path).create_img_pyramid()

            # Segmentation
            # s.get_segmentation(r=5, i=13, algo='SLIC')
            # Load segmentation
            # l.run_load_segmentation()
            
            # Write log of cene processed in csv            
            # with open(csv_path, 'a', newline='') as csvfile:
            #     logwriter = csv.writer(csvfile, delimiter=',')
            #     logwriter.writerow([sat.get_parameter_satellite()['initials_name'],
            #                         sat.get_parameter_satellite()[
            #         'aquisition_date'],
            #         sat.get_parameter_satellite()['index']])

            shutil.rmtree(tmp_dir)

            continue

        # Create objet to unpack files
        up = UF.UnpackFile(file_path=file_path, tmp_dir=tmp_dir)
        #####################################################################################
        ################################### Sentinel2 #######################################
        #####################################################################################
        # Bands: 2 = Blue | 3 = Green | 4 = Red | 8 = Nir |
        if sat.is_sentinel_file():
            # Unzip setinel file
            # up.uncompress_zip()

            # # Compose bands with 10m spatial resolution
            # CB.ComposeBands(input_dir=tmp_dir,
            #                 output_dir=tmp_dir,
            #                 output_file_name=sat.get_output_file_name()) \
            #     .stack_sentinel(scene_file_name=sat.get_parameter_satellite()["scene_file_name"],
            #                     utm_zone=sat.get_parameter_satellite()["index"])

            # # Reproject to Sirgas 2000
            # input_img_path = os.path.join(
            #     tmp_dir, f'{output_file_name}.TIF')
            # output_img_path = os.path.join(
            #     tmp_dir, f"r{output_file_name}.TIF")

            # rprj = RR.RasterReproject(input_img_path, output_img_path)
            # rprj.reproject_raster_to_epsg4674()

            # # Clip
            # img_path = f"{tmp_dir}/r{output_file_name}.TIF"

            # c = CR.ClipRaster(img_path=img_path, tmp_dir=tmp_dir,
            #                   scene_file_name=parameter_satellite["scene_file_name"],
            #                   output_dir=output_dir,
            #                   output_file_name=output_file_name)

            # r = R.Raster(img_path=img_path)

            
            # if r.intersects_trace_outline_aoi():
            #     c.clip_raster_by_mask(band_order=[4, 3, 2, 1])
            # else:
            #     import RasterTranslate as RT
            #     rt = RT.RasterTranslate(img_path=img_path,
            #                             output_dir=output_dir,
            #                             output_file_name=output_file_name)
            #     rt.translate_8bit(band_order=[4, 3, 2, 1])

            # # Make pyramid
            # img_path = os.path.join(
            #     output_dir, f"{output_file_name}.TIF")
            # PR.PyramidRaster(img_path=img_path).create_img_pyramid()

            # Segmentation
            # s.get_segmentation(r=10, i=10, algo='SLICO')
            # l.run_load_segmentation()

            # Cloud/Shadow
            
            # Save datetime when file was processed
            save_datetime_file_processig(parameter_satellite["scene_file_name"])

            shutil.rmtree(tmp_dir)
            
            continue
        #####################################################################################
        ################################### Landsat 8 #######################################
        #####################################################################################
        elif sat.get_parameter_satellite()['initials_name'] == 'LC08':
            # Set bands to unpack from landsat 8
            bands = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11]
            # Stack images
            # Bands: 3 = Green | 4 = Red | 5 = Nir | 6 = Swir1 |
            bands_expression = '3-6'
            # Clip
            band_order = [3, 2, 1, 4]

        #####################################################################################
        ################################### Landsat 5/7 #####################################
        #####################################################################################
        elif sat.is_landsat_file():
            # Set bands to unpack from landsat 5 and 7
            bands = [2, 3, 4, 5]
            # Stack images
            # Bands: 2 = Green | 3 = Red | 4 = Nir | 5 = Swir |
            bands_expression = '2-5'
            # Clip
            band_order = [3, 2, 1, 4]

        # Unpack files from landsat
        up.uncompres_file(bands)

        # Stack bands from landsat
        expression = f"L[C,T,E]0[5,7,8]*_B[{bands_expression}].TIF"
        CB.ComposeBands(input_dir=tmp_dir,
                        output_dir=tmp_dir,
                        output_file_name=sat.get_output_file_name()) \
            .stack_img(expression=expression,
                       extension='.TIF')

        # Reproject to compose bands (3456) to Sirgas 2000
        input_img_path = os.path.join(
            tmp_dir, f"{output_file_name}.TIF")
        output_img_path = os.path.join(
            tmp_dir, f"r{output_file_name}.TIF")

        rprj = RR.RasterReproject(input_img_path, output_img_path)
        rprj.reproject_raster_to_epsg4674()

        # Clip
        img_path = f"{tmp_dir}/r{output_file_name}.TIF"

        c = CR.ClipRaster(img_path=img_path, tmp_dir=tmp_dir,
                          scene_file_name=parameter_satellite["scene_file_name"],
                          output_dir=output_dir,
                          output_file_name=output_file_name)

        r = R.Raster(img_path=img_path)

        # Only clip raster if it intersects limit of project
        if r.intersects_trace_outline_aoi():
            c.clip_raster_by_mask(band_order=band_order)
        else:
            import RasterTranslate as RT
            rt = RT.RasterTranslate(img_path=img_path, 
                                    output_dir=output_dir,
                                    output_file_name=output_file_name)
            rt.translate_8bit(band_order)

        # Make pyramid
        img_path = os.path.join(
            output_dir, f"{output_file_name}.TIF")
        PR.PyramidRaster(img_path=img_path).create_img_pyramid()

        # Segmentation
        if sat.get_parameter_satellite()['initials_name'] == 'LC08':

            # s.get_segmentation(r=5, i=10, algo='SLICO')

            # Load database
            l.run_load_segmentation()

            # Cloud/Shadow
            cloud = CL.CloudShadow(tmp_dir, output_dir, sat.get_scene_file_name(),
                                   sat.get_output_file_name())
            cloud.run_cloud_shadow_fmask()
            pass

        # Write log of scene processed in csv
        with open(csv_path, 'a', newline='') as csvfile:
            logwriter = csv.writer(csvfile, delimiter=',')
            logwriter.writerow([parameter_satellite['initials_name'],
                                parameter_satellite['aquisition_date'],
                                parameter_satellite['index']])
        
        dst = Path(sys.argv[1], 'Landsat/processada')
        shutil.move(file_path, dst=dst)
        
        shutil.rmtree(tmp_dir)
        
        continue
