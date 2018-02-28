import sys
import time
from ManagementImageProcessingDirectory import get_list_folder_name_from_processed_dir
import PreProcess2TA as Pre2TA



if __name__ == "__main__":

    # Runing pre-processing Landsat 8 repository for forest monitoring project to Bahia
    raster = Pre2TA.PreProcess2TA(raster_file_path_targz=sys.argv[1],
                                  set_output_processed_repo=sys.argv[2])

    # Check if tar.gz file have already processed before
    # Comparing if file name exist in list of folder name processed
    processed_folder = raster.get_folder_output_processed_path()
    folder_name_list_processed_file = get_list_folder_name_from_processed_dir(processed_folder)

    if raster.file_name_targz not in folder_name_list_processed_file:
        start = time.time()
        # raster.run_make_folder_input_data()
        # raster.run_cloud_shadow_fmask()
        raster.run_segmentation()
        print("Time processing: ", (time.time()-start)/60)
    else:
        print("Arquivo já processado")
