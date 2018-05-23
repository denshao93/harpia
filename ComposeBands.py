import os


class ComposeBands:

    def __init__(self, image_output_path_stored, scene_image_name, dir_tmp_img):
        # The folder where output processed will be saved
        self.image_output_path_stored = image_output_path_stored

        # Temporary folder to put files to process and remove after that
        self.dir_tmp_img = dir_tmp_img

        self.file_name = scene_image_name

        # Path where band files can be find.
        self.tmp_raw_img_path = os.path.join(self.dir_tmp_img, self.file_name)

    def stack_img(self, output_image_path, output_image_name, expression):
        """Stacking bands from landsat in tmp folder.
           The expression is the bands which will be stacked.

        Arguments:
            output_image_path {str} -- The path where image will be save.
            output_image_name {str} -- The name of image output with extention (ie. ref.img).
            expression {str} -- Regular expression which select files who will be put in output.
        """

        # Path where band files can be find.
        # Here, it is the input for gdal_merge.
        tmp_raw_img = os.path.join(self.tmp_raw_img_path, expression)

        # Output image
        output_image_path = os.path.join(output_image_path, output_image_name)

        command = "gdal_merge.py -of HFA -co COMPRESSED=YES -o {output_image} " \
                  "{tmp_raw_img}".format(output_image=output_image_path,
                                         tmp_raw_img=tmp_raw_img)

        os.system(command)

    def get_image_pyramid_from_stack_image_stored(self, image_path, image_name):

        print('...Pyramid...')
        image_path = os.path.join(image_path, image_name)
        command = "gdaladdo -r nearest {image} " \
                  "2 4 8 16 32 64 128 256 512 1024".format(image=image_path)

        os.system(command)

    def run_image_composition(self):

        self.stack_img(output_image_path=self.dir_tmp_img,
                       output_image_name="ref.img",
                       expression="LC08*_B[1-7,9].TIF")
        self.stack_img(self.dir_tmp_img, "thermal.img", "LC08*_B1[0,1].TIF")
        self.stack_img(self.image_output_path_stored, self.file_name + ".TIF", expression="LC08*_B[3-5].TIF")
        self.get_image_pyramid_from_stack_image_stored( image_path=self.image_output_path_stored,
                                                        image_name=self.file_name + ".TIF")

