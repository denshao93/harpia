import sys
import os
import ManagementDirectory as md

if __name__ == "__main__":

    # Runing pre-processing Landsat 8 repository for forest monitoring project to Bahia
    # raster = Pre2TA.PreProcess2TA(raster_file_path_targz=sys.argv[1],
    #                               set_output_processed_repo=sys.argv[2])

    # TODO Adicionar o loop para colocar todos os arquivos tar.gz para rodar
    # Check if tar.gz file have already processed before
    # Comparing if file name exist in list of folder name processed

    for subdir, dirs, files in os.walk(sys.argv[1]):
        for file in files:
            # print os.path.join(subdir, file)
                if file.endswith(".tar.gz"):
                    print(file)
                    file_path = subdir + os.sep + file

                    mdir = md.ManagementDirectory(dir_all_targz=sys.argv[1],
                                                  output_root_dir_image_processed=sys.argv[2],
                                                  raster_file_path_targz=file_path)

                    mdir.run_manage_directory()

