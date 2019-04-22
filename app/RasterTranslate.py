import os

class RasterTranslate:
    def __init__(self, img_path, output_file_name, output_dir):
        
        self.img_path = img_path

        self.output_file_name = os.path.join(output_dir, f"{output_file_name}.TIF")
    
    def translate_8bit(self, band_order=None):
        
        red = band_order[0]
        green = band_order[1]
        blue = band_order[2]
        
        if len(band_order) < 4:
            command = f"gdal_translate {self.img_path} -ot Byte -scale " \
                f"{self.output_file_name} -a_nodata 0 "\
                f"-b {red} -b {green} -b {blue} --config " \
                f"GDAL_CACHEMAX 1000 --config GDAL_NUM_THREADS ALL_CPUS " \
                f"-co COMPRESS=DEFLATE -co ALPHA=NO"
        else:
            last = band_order[3]

            command = f"gdal_translate {self.img_path} -ot Byte -scale " \
                    f"{self.output_file_name} -a_nodata 0 "\
                    f"-b {red} -b {green} -b {blue} -b {last} --config " \
                    f"GDAL_CACHEMAX 1000 --config GDAL_NUM_THREADS ALL_CPUS " \
                    f"-co COMPRESS=DEFLATE -co ALPHA=NO"
        os.system(command)
        