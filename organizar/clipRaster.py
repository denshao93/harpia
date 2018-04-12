import os


def clip_raster_by_mask():
    command = "gdalwarp -cutline /media/dogosousa/1AF3820C0AA79B17/monitor_floresta/LC8/215068/215068_WGS24N.shp " \
              "-crop_to_cutline -dstnodata -999.0 /tmp/LC08_L1TP_215068_20160913_20170321_01_T1/ref.img " \
              "/tmp/LC08_L1TP_215068_20160913_20170321_01_T1/cut.tif"
    os.system(command)

clip_raster_by_mask()