import PreProcess2TA as Pre2TA
import sys
import time


if __name__ == "__main__":

    # Runing CloudShadowFmask for Landsat 8 repository
    start = time.time()
    raster = Pre2TA.PreProcess2TA(raster_file_path_targz=sys.argv[1],
                                  set_output_processed_repo=sys.argv[2])
    # raster.run_make_folder_input_data()
    # raster.run_cloud_shadow_fmask()
    raster.run_segmentation()

    print("Time processing: ", (time.time()-start)/60)
