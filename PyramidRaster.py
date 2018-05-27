import os


class PyramidRaster(object):

    def __init__(self, image_folder_stored, image_name_stored):

        # The folder where output processed will be saved
        self.image_folder_stored = image_folder_stored

        self.image_name_stored = image_name_stored

        self.image_path_stored = os.path.join(self.image_folder_stored, self.image_name_stored+".TIF")

    def get_image_pyramid_from_stack_image_stored(self):

        print('...Pyramid...')

        command = "gdaladdo -r nearest {image} " \
                  "2 4 8 16 32 64 128 256 512 1024".format(image=self.image_path_stored)

        os.system(command)

    def run_pyramid(self):

        # Creating pyramid for image stored
        self.get_image_pyramid_from_stack_image_stored()