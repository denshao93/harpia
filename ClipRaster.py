import os


def clip_raster_by_mask():
    # vetor = "/vetor/lc8_ba_32624_buffer.shp"
    command = "gdalwarp -cutline /home/diogocaribe/Projetos/preprocess2ta/vetor/lc8_ba_4674_buffer.shp -crop_to_cutline -dstnodata 0 "\
              "/tmp/tmpz__mgdje/ref.img /tmp/tmpz__mgdje/cut_ref.TIF"
    os.system(command)

clip_raster_by_mask()