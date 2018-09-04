import os
import fiona
import rasterio
import numpy as np
import Raster as R
import rasterio.mask
import geo_utils as gu
from shapely import wkt
from rasterio.warp import calculate_default_transform, reproject, Resampling

class ClipRaster:

    def __init__(self, img_path, tmp_dir, scene_file_name,
                 output_dir, output_file_name):
        
        self.image_path = img_path

        self.tmp_dir = tmp_dir

        self.scene_file_name = scene_file_name

        self.output_dir = output_dir

        self.output_file_name = output_file_name
    
    #Transform to uint8
    @staticmethod
    def scale8bit(image):
        scale = float(256) / (image.max() - image.min())
        return np.clip(np.round(np.multiply(image, scale)), 0, 255).astype(np.uint8)

    def clip_raster_by_mask(self, band_order):
        print(".........Clip raster..........")
        
        with fiona.open("/home/diogo.sousa/workspace/harpia/data/vector/ba_4674_buffer.shp", "r") as shapefile:
            features = [feature["geometry"] for feature in shapefile]
        
        with rasterio.open(f"{self.tmp_dir}/r{self.output_file_name}.TIF") as src:
            out_image, out_transform = rasterio.mask.mask(src, features, crop=True)
            out_meta = src.meta.copy()
            out_meta.update({"driver": "GTiff",
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "transform": out_transform,
                "alpha": 'NO',
                "COMPRESS": 'DEFLATE',
                "PHOTOMETRIC": 'RGB',
                "dtype": "uint8"})
            out_image = self.scale8bit(out_image)
        
        with rasterio.open(f"{self.output_dir}/{self.output_file_name}.TIF", "w", **out_meta) as dest:
            # Set order bands to save (NIR/GREEN/RED/BLUE)
            # This bands not the same in LC08
            dest.write(out_image, band_order) 

    def run_clip(self, band_order):
        """
        band_order = ex. [4,3,2,1]
        """
        self.clip_raster_by_mask(band_order)