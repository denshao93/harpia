import os

class RasterTranslate:
    def __init__(self, img_path, output_file_name, output_dir):
        
        self.img_path = img_path

        self.output_file_name = os.path.join(output_dir, f"{output_file_name}.TIF")
    
    def translate_8bit(self):

        command = f"gdal_translate {self.img_path} -ot Byte -scale " \
                  f"{self.output_file_name} -a_nodata 0 -b 4 -b 3 -b 2 -b 1 --config " \
                  f"GDAL_CACHEMAX 1000 --config GDAL_NUM_THREADS ALL_CPUS " \
                  f"-co COMPRESS=DEFLATE -co ALPHA=NO"
        os.system(command)
        