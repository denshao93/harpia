import os
import fiona
import rasterio
import Raster as R
import rasterio.mask
import geo_utils as gu
from shapely import wkt


class ClipRaster:

    def __init__(self, img_path, tmp_dir, scene_file_name,
                 output_dir, output_file_name):
        
        self.image_path = img_path

        self.tmp_dir = tmp_dir

        self.scene_file_name = scene_file_name

        self.output_dir = output_dir

        self.output_file_name = output_file_name

    def check_img_will_be_cliped(self):
        """Verify if image have to be cliped.

        If img overlap boundery of area of interested project (aoi),
        It should be cliped to remove image that not be useless.
        This processing avoid to save raster useless areas.

        """
        ba_line = gu.read_shapefile_poly("/home/diogocaribe/workspace/harpia/vector/ba_4674_line.shp")
        trace_outline = R.Raster(self.image_path).trace_outline_from_raster_wkt()
        trace_outline = wkt.loads(trace_outline)

        check_intersects = trace_outline.intersects(ba_line)

        return check_intersects

    def clip_raster_by_mask(self):
        
        with fiona.open("/home/diogocaribe/workspace/harpia/vector/ba_4674_buffer.shp", "r") as shapefile:
            features = [feature["geometry"] for feature in shapefile]
        
        with rasterio.open(f"{self.tmp_dir}/r{self.output_file_name}.TIF") as src:
            out_image, out_transform = rasterio.mask.mask(src, features, crop=True)
            out_meta = src.meta.copy()
        out_meta.update({"driver": "GTiff",
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "transform": out_transform})
        with rasterio.open(f"{self.output_dir}/{self.output_file_name}.TIF", "w", **out_meta) as dest:
            dest.write(out_image)

   
    def reproject_raster_to_epsg4674(self):

        command =   f"gdalwarp -t_srs EPSG:4674 -multi -dstnodata 0 "\
                    f"{self.tmp_dir}/{self.output_file_name}.TIF "\
                    f"{self.tmp_dir}/r{self.output_file_name}.TIF"

        os.system(command)

    def cut_gdal(self):
        
        vector = "/home/diogocaribe/workspace/harpia/vector/ba_4674_buffer.shp"

        command = f"gdalwarp -cutline {vector} -crop_to_cutline -multi " \
                  f"-dstnodata 0 {self.tmp_dir}/r{self.output_file_name}.TIF "\
                  f"{self.tmp_dir}/c{self.output_file_name}.TIF"
        
        os.system(command)

    def compress_save_output_raster(self):
        
        command = f"gdal_translate -ot Byte -scale -co compress=DEFLATE -b 4 -b 3 -b 2 -b 1"\
                  f"-multi -a_nodata 0 {self.tmp_dir}/c{self.output_file_name}.TIF "\
                  f"{self.output_dir}/{self.output_file_name}.TIF"
        
        os.system(command)

    def run_clip_(self):
        self.reproject_raster_to_epsg4674()
        self.clip_raster_by_mask()

    def run_clip(self):
        self.reproject_raster_to_epsg4674()
        self.cut_gdal()
        self.compress_save_output_raster()
