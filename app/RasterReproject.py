import os

class RasterReproject:
    
    def __init__(self, tmp_dir, output_file_name):
        
        self.tmp_dir = tmp_dir

        self.output_file_name = output_file_name
        
    def reproject_raster_to_epsg4674(self):

        command =   f"gdalwarp -t_srs EPSG:4674 -wo NUM_THREADS=ALL_CPUS "\
                    f"-wo SOURCE_EXTRA=1000 --config GDAL_CACHEMAX 500 -wm 500 "\
                    f"{self.tmp_dir}/{self.output_file_name}.TIF "\
                    f"{self.tmp_dir}/r{self.output_file_name}.TIF"

        os.system(command)