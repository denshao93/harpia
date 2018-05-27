import os
import sys
import utils as u
import PyramidRaster as Pyramind
import ClipRaster as Clip
import CloudShadow as Cs
import Segmetation as Seg
import ComposeBands as Compose
import UncompressFile as Un
import OrganizeDirectory as Od
from SatelliteFileInfo import LandsatFileInfo as LCinfo
import Connection2Database as con

if __name__ == "__main__":

    # Running pre-processing Landsat 8 repository for forest monitoring project to Bahia
    for subdir, dirs, files in os.walk(sys.argv[1]):
        for file in files:
            if file.endswith(".tar.gz"):
                print("Processing "+file)
                # Variables
                file_path_targz = os.path.join(subdir, file)
                # The name of file with all parameters from tar.gz downloaded
                full_image_scene_name = u.file_name_without_extention(file_path_targz)

                # The name of image that will be save. Not all parameters will be saved in file name.
                img_file_name_stored = '{}{}'.format(full_image_scene_name[:5],
                                                       full_image_scene_name[10:25])

                # Ordering directory to receive results
                mdir = Od.OrganizeDirectory(output_root_dir_image_processed=sys.argv[2],
                                            image_file_path_targz=file_path_targz)

                # The path where processed image (results) will be saved
                img_output_path_stored = mdir.create_dir_satellite_year_pathrow_image()
                mdir.run_manage_directory()

                # Uncompressing file which has landsat bands
                uncompress = Un.UncompressFile(image_file_path_targz=file_path_targz,
                                               file_name=full_image_scene_name)
                uncompress.run()

                # Temporary directory where image files were stored to be processed
                dir_tmp_img = uncompress.dir_tmp_img

                # Creating image stacking from landsat bands
                compose = Compose.ComposeBands(image_output_path_stored=img_output_path_stored,
                                           scene_image_name=full_image_scene_name,
                                           dir_tmp_img=dir_tmp_img)
                compose.run_image_composition()

                # Clip raster
                Clip.ClipRaster(scene_image_name=full_image_scene_name,
                              dir_tmp_img=dir_tmp_img,
                              img_output_path_stored=img_output_path_stored,
                              img_file_name_stored=img_file_name_stored).run()

                # Creating pyramid to image stored
                pyramid = Pyramind.PyramidRaster(image_folder_stored=img_output_path_stored,
                                                image_name_stored=img_file_name_stored).run_pyramid()

                # Processing cloud shadow fmask
                cloud = Cs.CloudShadow(dir_tmp_img=dir_tmp_img,
                                        image_output_path=img_output_path_stored,
                                        file_name=full_image_scene_name)
                cloud.run_cloud_shadow_fmask()

                # Segmentation
                s = Seg.Segmentation(img_output_path_stored=img_output_path_stored,
                                    file_name=full_image_scene_name)
                s.run_segmentation()

                # Getting information from Landsat image file
                # lcinfo = LCinfo(file_name=file_name)
                # path_row = '{path}{row}'.format(path=lcinfo.get_path_row_from_file()[0],
                #                                 row=lcinfo.get_path_row_from_file()[1])
                # satellite_name = lcinfo.get_satellite_name()

                # Creating schema where segmentation will be load
                # conn = con.Connection("host=localhost dbname=ta7_rascunho \
                #                         user=postgres password=postgres")
                # conn.create_scene_path_row_schema(satellite_name=satellite_name,
                #                                     path_row=path_row)

                # conn.create_table_scene_path_row_scene(satellite_name=satellite_name,
                #                                         path_row=path_row, file_name=file_name)
                # conn.del_table_scene_path_row_scene(satellite_name=satellite_name,
                #                                     path_row=path_row, file_name=file_name)
                # shapefile_path = '{image_output_path}/{file_name}.shp'.format(image_output_path=image_output_path,
                #                                                                 file_name=file_name)
                # conn.load_segmentation_database(satellite_name=satellite_name,
                #                                 path_row=path_row, file_name=file_name,
                #                                 shapefile_path=shapefile_path)


