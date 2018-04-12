import os
import sys
import utils as u
import CloudShadow as Cs
import ComposeBands as Cmp
import OrganizeDirectory as Od
import UncompressFile as Uc


if __name__ == "__main__":

    # Runing pre-processing Landsat 8 repository for forest monitoring project to Bahia

    # Check if tar.gz file have already processed before
    # Comparing if file name exist in list of folder name processed

    for subdir, dirs, files in os.walk(sys.argv[1]):
        for file in files:
                if file.endswith(".tar.gz"):

                    file_path_targz = os.path.join(subdir, file)
                    scene_image_name = u.file_name_without_extention(file_path_targz)

                    # Ordering directory to receive results
                    mdir = Od.OrganizeDirectory(output_root_dir_image_processed=sys.argv[2],
                                                image_file_path_targz=file_path_targz)
                    mdir.run_manage_directory()

                    # The path where processed image (results) will be saved
                    image_output_path = mdir.create_dir_satellite_year_pathrow_image()

                    # Uncompressing file which has landsat bands
                    uncompress = Uc.UncompressFileAsEpsg4674(image_file_path_targz=file_path_targz)
                    uncompress.run()
                    dir_tmp_img = uncompress.dir_tmp_img

                    # Creating image stacking from landsat bands
                    compose = Cmp.ComposeBands(image_output_path=image_output_path,
                                               scene_image_name=scene_image_name,
                                               dir_tmp_img=dir_tmp_img)
                    compose.run_image_composition()

                    # Processing cloud shadow fmask
                    cloud = Cs.CloudShadow(dir_tmp_img=dir_tmp_img,
                                           image_output_path=image_output_path,
                                           file_name=scene_image_name)
                    cloud.run_cloud_shadow_fmask()

                    # Segmentation
