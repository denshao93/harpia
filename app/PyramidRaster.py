import os


class PyramidRaster(object):

    def __init__(self, img_path):

        self.img_path = img_path

    def create_img_pyramid(self):

        print('...Pyramid...')

        command = f"gdaladdo -r nearest {self.img_path} "\
                  f"2 4 8 16 32 64 128 256 512 1024"

        os.system(command)
