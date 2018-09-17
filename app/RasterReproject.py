import os

class RasterReproject:
    
    def __init__(self, input_img_path, output_img_path):
        
        self.input_img_path = input_img_path

        self.output_img_path = output_img_path
        
    def reproject_raster_to_epsg4674(self):

        command =   f"gdalwarp -t_srs EPSG:4674 -wo NUM_THREADS=ALL_CPUS "\
                    f"-wo SOURCE_EXTRA=1000 --config GDAL_CACHEMAX 500 -wm 500 "\
                    f"{self.input_img_path} "\
                    f"{self.output_img_path}"

        os.system(command)