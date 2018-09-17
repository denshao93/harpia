import os
import shutil
import Raster as R
import ClipRaster as CR
import RasterReproject as RR

class CloudShadow:

    def __init__(self,
                 tmp_dir,
                 output_dir,
                 scene_file_name,
                 output_file_name):

        self.scene_file_name = scene_file_name

        self.tmp_dir = tmp_dir

        self.output_dir = output_dir

        self.output_file_name = output_file_name

    def compose_bands_oli(self):
        print(".....Compose OLI....")
        command = f"gdal_merge.py -separate -of HFA -co COMPRESSED=YES "\
                  f"-o {self.tmp_dir}/ref.img {self.tmp_dir}/LC08*_B[1-7,9].TIF"
        os.system(command)
    
    def compose_bands_thermal(self):
        print(".....Compose Thermal....")
        command = f"gdal_merge.py -separate -of HFA -co COMPRESSED=YES "\
                  f"-o {self.tmp_dir}/thermal.img {self.tmp_dir}/LC08*_B1[0,1].TIF"
        os.system(command)

    def create_angle_img(self):
        print(".....Creating angle image....")
        command = f"fmask_usgsLandsatMakeAnglesImage.py -m "\
                  f"{self.tmp_dir}/{self.scene_file_name}*_MTL.txt -t {self.tmp_dir}/ref.img "\
                  f"-o {self.tmp_dir}/angles.img"
        os.system(command)

    def saturation_mask(self):
        print(".....Creating saturation image....")
        command = f"fmask_usgsLandsatSaturationMask.py -i {self.tmp_dir}/ref.img "\
                  f"-m {self.tmp_dir}/{self.scene_file_name}*_MTL.txt"\
                  f" -o {self.tmp_dir}/saturationmask.img"
        os.system(command)

    def landsat_toa(self):
        print(".....Creating TOA image....")
        command = f"fmask_usgsLandsatTOA.py -i {self.tmp_dir}/ref.img -m "\
                  f"{self.tmp_dir}/{self.scene_file_name}*_MTL.txt -z {self.tmp_dir}/angles.img " \
                  f"-o {self.tmp_dir}/toa.img"
        os.system(command)

    def cloud_detection(self):
        print(".....Creating cloud detection image....")
        command = f"fmask_usgsLandsatStacked.py -t {self.tmp_dir}/thermal.img -a "\
                  f"{self.tmp_dir}/toa.img -m {self.tmp_dir}/{self.scene_file_name}*_MTL.txt " \
                  f"-z {self.tmp_dir}/angles.img -s {self.tmp_dir}/saturationmask.img "\
                  f"-o {self.tmp_dir}/c{self.scene_file_name}.tif"
        os.system(command)
    
    def reproject_cloud_detection(self):
        # Reproject to compose bands (3456) to Sirgas 2000 
        input_img_path = os.path.join(self.tmp_dir, f"c{self.scene_file_name}.tif")
        output_img_path = os.path.join(self.tmp_dir, f"rc{self.scene_file_name}.tif")
            
        rprj = RR.RasterReproject(input_img_path, output_img_path)
        rprj.reproject_raster_to_epsg4674()
    
    def clip_cloud(self):
        
        # Clip

        # Cloud reprojected file
        rc = os.path.join(self.tmp_dir, f"rc{self.scene_file_name}.tif")
        
        r = R.Raster(img_path=rc)
        
        # Only clip raster if it intersects limit of project
        if r.intersects_trace_outline_aoi():
            
            c = CR.ClipRaster(img_path=rc, tmp_dir=self.tmp_dir, 
                        scene_file_name=self.scene_file_name,
                        output_dir = self.output_dir, 
                        output_file_name = f"c{self.output_file_name}.TIF")
            
            c.clip_raster_by_mask()
        else:
            dst = os.path.join(self.output_dir, f"c{self.scene_file_name}.tif")
            shutil.move(src=rc, dst=dst)

    def run_cloud_shadow_fmask(self):
        """
        Run fsmak that will return classification of image processed which have five classes (cloud, shadow, water,
         "soil")
        The output will be raster and vectorda
        :return:
        """
        self.compose_bands_oli()
        self.compose_bands_thermal()
        self.create_angle_img()
        self.saturation_mask()
        self.landsat_toa()
        self.cloud_detection()
        self.reproject_cloud_detection()
        self.clip_cloud()


# if __name__ == '__main__':

    
#     c = CloudShadow(tmp_dir="/tmp/tmpne7c6khj", output_dir,
#                  scene_file_name,
#                  output_file_name):

