import os
import sys
import utils as u
import CloudShadow as Cs
import Segmetation as Seg
import ClipRaster as Clip
import UncompressFile as Un
import ComposeBands as Compose
import OrganizeDirectory as Od
import PyramidRaster as Pyramind
import Connection2Database as con
import LoadSegmentationDatabase as LSegDB
from SatelliteFileInfo import LandsatFileInfo as LCinfo


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
                segmentation_file_path = os.path.join(img_output_path_stored,
                                                      img_file_name_stored+"_SLIC.shp" )
                load_seg = LSegDB.LoadSegmentationDatabase(segmentation_file_path=segmentation_file_path,
                                    full_scene_name=full_image_scene_name,
                                    img_file_name_stored=img_file_name_stored)
                load_seg.run_load_segmentation()


