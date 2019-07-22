import csv
# import datetime
import glob
import os 
import pathlib
import shutil
import sys
import tempfile
from datetime import datetime
from pathlib import Path

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

OUTPUT_FOLDER_NAME = 'PROCESSADA'
INPUT_FOLDER_NAME = 'BRUTA'

path_home = pathlib.Path.home()

path_cwd = pathlib.Path.cwd()

datetime_now = datetime.now()

# Open yaml 
with open(path_cwd/'app/config/const.yaml', 'r') as f:
        const = yaml.safe_load(f)

# Params to connect to postgres database
conn_string = const['db']


def file_list_not_process():
    """Create list of files wich not processed
    """
    con = C.Connection(conn_string)
    query = f"SELECT title FROM metadado_img.metadado_sentinel WHERE "\
            f"date_file_processing IS NULL AND date_download_img NOTNULL " \
            f"ORDER BY substring(title, 40 , 5), substring(title, 12 , 8);"
    file_list = con.run_query(query)
    file_list = [i[0] for i in file_list]
    return file_list


def get_file_path(file_name):

    return path_home/INPUT_FOLDER_NAME/file_name


def save_datetime_img_processing(scene_title):
    """Update database field where save datetime when img was processed
    
    Parameters
    ----------
    scene_title : [str]
        Title from file of satellite image
    """
    con = C.Connection(conn_string)
    query = f"UPDATE metadado_img.metadado_sentinel SET date_file_processing =" \
            f"current_timestamp WHERE title = '{scene_title}';"
    return con.run_update(query)


def create_task_terraamazon_poject(conn_string: str, 
                            aquisition_date: str, 
                            satellite_name: str,
                            satellite_index: str):
    """
        -- aqui retorna o id para o aoi_layer_id (ta_catalog)
        select * from terraamazon.ta_aoi_layer  

        -- insere dados na tabela de cenas
        insert into ta_scene (view_date, julday, inclusion,ai_object_id, aoi_layer_id)
        select  to_date('02/01/2018','dd/mm/yyyy'), extract(doy from to_date('02/01/2018','dd/mm/yyyy')), current_timestamp(0), 1, 40 
    """
    con = C.Connection(conn_string)
    
    view_date = datetime.strptime(aquisition_date, '%Y%m%d').strftime('%Y-%m-%d')

    # O ai_object_id é o pathrow, tile.
    ai_object_id = satellite_index
    
    # É o id do terraamazon.ta_catalog.
    aoi_layer_id_query = f"SELECT id FROM terraamazon.ta_catalog WHERE name LIKE '%{satellite_name}%';"
    aoi_layer_id = con.run_query(aoi_layer_id_query)[0][0]

    check_if_task_was_created_query = f"SELECT * FROM terraamazon.ta_scene WHERE view_date = '{view_date}' AND ai_object_id = '{ai_object_id}';"
    check_if_task_was_created = len(con.run_query(check_if_task_was_created_query)) == 0
    
    if check_if_task_was_created:

        insert_query = f"INSERT INTO terraamazon.ta_scene (view_date, julday, inclusion, ai_object_id, aoi_layer_id) " \
                f"select  to_date('{view_date}','yyyy-mm-dd'), extract(doy from to_date('{view_date}', 'yyyy-mm-dd')), " \
                f" current_timestamp(0), '{ai_object_id}', {aoi_layer_id};"

        return con.run_query(insert_query)


def add_task_to_terraamazon_project(conn_string: str, 
                            aquisition_date: str, 
                            satellite_index: str,
                            project_name: str):
    """
    -- insere dado na tabela que amarra a cena ao projeto, para criar a tarefa.
        insert into terraamazon.ta_project_scene (project_id, scene_id, locked) values (1,1,false)
    """
    con = C.Connection(conn_string)
    
    view_date = datetime.strptime(aquisition_date, '%Y%m%d').strftime('%Y-%m-%d')
    
    project_id_query = f"SELECT id FROM terraamazon.ta_project WHERE name LIKE '{project_name}';"
    project_id = con.run_query(project_id_query)[0][0]

    # id scene_id
    scene_id_query = f"SELECT id FROM terraamazon.ta_scene WHERE ai_object_id = '{satellite_index}' AND view_date = '{view_date}';"
    scene_id = con.run_query(scene_id_query)[0][0]

    check_if_task_in_project_query = f"SELECT * FROM terraamazon.ta_project_scene WHERE project_id = '{project_id}' AND scene_id = '{scene_id}';"
    check_if_task_in_project = len(con.run_query(check_if_task_in_project_query)) == 0
    
    if check_if_task_in_project:
        insert_query = f"INSERT INTO terraamazon.ta_project_scene (project_id, scene_id, locked) values ({project_id}, {scene_id},false)"

        con.run_query(insert_query) 


def cloud_shadow(input_file, output_dir, ouput_file_name):
    cloud = CL.CloudShadow(tmp_dir, output_dir, sat.get_scene_file_name(),
                                   sat.get_output_file_name())
    cloud.run_cloud_shadow_fmask_landsat()


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
 
    files = file_list_not_process()
   
    for file in files:
        file_path = f"{get_file_path(file_name=file)}.zip"
    
        # Create tmp director to put all temp files
        tmp_dir = tempfile.mkdtemp()

        # Create instance of landsat file where scene features are
        sat = SFI.SatelliteFileInfo(file_path)

        parameter_satellite = sat.get_parameter_satellite()
        output_file_name = sat.get_output_file_name()
        scene_file_name = parameter_satellite["scene_file_name"]
       
        # Create director where files will be saved
        od = OD.OrganizeDirectory(root_dir_path=sys.argv[2],
                                  satellite_name=parameter_satellite["initials_name"],
                                  satellite_index=parameter_satellite["index"],
                                  year=parameter_satellite["aquisition_year"],
                                  month=parameter_satellite["aquisition_month"],
                                  file_name=parameter_satellite["scene_file_name"])

        # Create directory to save results
        output_dir = od.create_output_dir()

         # Create objet to unpack files
        up = UF.UnpackFile(file_path=file_path, tmp_dir=tmp_dir)

        #####################################################################################
        ################################### Sentinel2 #######################################
        #####################################################################################
        # Bands: 2 = Blue | 3 = Green | 4 = Red | 8 = Nir |
        if sat.is_sentinel_file():
            
            aquisition_date = parameter_satellite['aquisition_date']
            # satellite_name
            if sat.is_sentinel_file():
                satellite_name = 'sentinel'
            satellite_index = sat.get_parameter_satellite()["index"]
            
            # Unzip setinel file
            up.uncompress_zip()

            # Compose bands with 10m spatial resolution
            CB.ComposeBands(input_dir=tmp_dir,
                            output_dir=tmp_dir,
                            output_file_name=sat.get_output_file_name()) \
                .stack_sentinel(scene_file_name=sat.get_parameter_satellite()["scene_file_name"],
                                utm_zone=sat.get_parameter_satellite()["index"])

            # Reproject to Sirgas 2000
            input_img_path = os.path.join(
                tmp_dir, f'{output_file_name}.TIF')
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

            
            if r.intersects_trace_outline_aoi():
                c.clip_raster_by_mask(band_order=[1, 2, 3])
            else:
                import RasterTranslate as RT
                rt = RT.RasterTranslate(img_path=img_path,
                                        output_dir=output_dir,
                                        output_file_name=output_file_name)
                rt.translate_8bit(band_order=[1, 2, 3])

            # Make pyramid
            img_path = os.path.join(
                output_dir, f"{output_file_name}.TIF")
            PR.PyramidRaster(img_path=img_path).create_img_pyramid()
            
            create_task_terraamazon_poject(conn_string,  aquisition_date, satellite_name, satellite_index)
            add_task_to_terraamazon_project(conn_string,  aquisition_date, satellite_index, project_name='MONITORAMENTO')
            
             # Save when file was processed in postgres database
            save_datetime_img_processing(scene_title=parameter_satellite["scene_file_name"])

            shutil.rmtree(tmp_dir)
            
            continue
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

        # Cloud/Shadow
        if sat.get_parameter_satellite()['initials_name'] == 'LC08':

            cloud = CL.CloudShadow(tmp_dir, output_dir, sat.get_scene_file_name(),
                                   sat.get_output_file_name())
            cloud.run_cloud_shadow_fmask_landsat()
            pass
        
        dst = Path(sys.argv[1], 'Landsat/processada')
        shutil.move(file_path, dst=dst)
        
        shutil.rmtree(tmp_dir)
        
        continue
