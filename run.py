import os
import sys
import utils as u
import UncompressFileAsEpsg4674 as uncp
import ComposeBands as cmp
import OrganizeDirectory as md

if __name__ == "__main__":

    # Runing pre-processing Landsat 8 repository for forest monitoring project to Bahia

    # TODO ver se o arquivos já foi processado. Só processar aquilo que nunca foi processado
    # Check if tar.gz file have already processed before
    # Comparing if file name exist in list of folder name processed

    for subdir, dirs, files in os.walk(sys.argv[1]):
        for file in files:
                if file.endswith(".tar.gz"):
                    print(file)
                    file_path_targz = os.path.join(subdir, file)
                    scene_image_name = u.file_name_without_extention(file_path_targz)

                    mdir = md.OrganizeDirectory(output_root_dir_image_processed=sys.argv[2],
                                                image_file_path_targz=file_path_targz)

                    mdir.run_manage_directory()

                    # The path from processed image
                    image_output_path = mdir.create_dir_satellite_year_pathrow_image()

                    uncompress = uncp.UncompressFileAsEpsg4674(image_file_path_targz=file_path_targz)
                    uncompress.run()

                    dir_tmp_img_epsg_4674 = uncompress.dir_tmp_img_epsg_4674

                    compose = cmp.ComposeBands(image_output_path=image_output_path,
                                               scene_image_name=scene_image_name,
                                               tmp_reprojected=dir_tmp_img_epsg_4674)
                    compose.run_image_composition()





