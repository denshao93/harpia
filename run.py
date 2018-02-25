import PreProcess2TA as csf
import sys
import time


if __name__ == "__main__":

    # Runing CloudShadowFmask for Landsat 8 repository
    start = time.time()
    raster = csf.PreProcess2TA(raster_file_path_targz=sys.argv[1],
                               set_output_processed_repo=sys.argv[2])
    img = raster.run_cloud_shadow_fmask()
    print("Time processing: ", (time.time()-start)/60)
