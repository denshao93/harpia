import sys
import os
import ManagementDirectory as md

if __name__ == "__main__":

    # Runing pre-processing Landsat 8 repository for forest monitoring project to Bahia

    # TODO ver se o arquivos já foi processado. Só processar aquilo que nunca foi processado
    # Check if tar.gz file have already processed before
    # Comparing if file name exist in list of folder name processed

    for subdir, dirs, files in os.walk(sys.argv[1]):
        for file in files:
                if file.endswith(".tar.gz"):
                    print(file)
                    file_path = os.path.join(subdir, file)

                    mdir = md.ManagementDirectory(dir_all_targz=sys.argv[1],
                                                  output_root_dir_image_processed=sys.argv[2],
                                                  image_file_path_targz=file_path)

                    mdir.run_manage_directory()


                    # The path from processed image
                    image_output = mdir.create_dir_satellite_year_pathrow_image()





